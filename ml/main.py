from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn, os, pickle
import numpy as np
from sklearn.ensemble import IsolationForest


PORT = 8000                 
MODEL_PATH = "./model.pkl"  
IF_TREES = 100              
IF_CONTAM = 0.05            


_features_order = ["acctAgeHours", "device24h", "ip10m", "user24h", "value"]

_center = np.array([100.0, 1.0, 0.0, 0.0, 5.0], dtype=float)

app = FastAPI()
_model = None

# --- Startup logger ---
@app.on_event("startup")
def _startup_log():
    try:
        route_paths = [getattr(r, "path", str(r)) for r in app.routes]
        print(f"[ml] FastAPI starting from: {__file__}")
        print(f"[ml] Registered routes: {route_paths}")
    except Exception as e:
        print("[ml] startup log failed:", e)

# ---- Schemas ----
class ScoreIn(BaseModel):
    couponValue: Optional[float] = None
    acctAgeHours: Optional[float] = None
    device_redemptions24h: Optional[float] = None
    ip_uniqueAccounts10m: Optional[float] = None
    user_redemptions24h: Optional[float] = None
    features: Optional[Dict[str, float]] = None
    X: Optional[List[float]] = None  

class TrainIn(BaseModel):
    legit: List[Dict[str, float]] = []
    abuse: List[Dict[str, float]] = []  

# ---- Helpers ----
def _as_float(x: Optional[float]) -> float:
    try:
        return float(x) if x is not None else 0.0
    except Exception:
        return 0.0

def _extract_vector(inp: ScoreIn) -> np.ndarray:

    if inp.X:
        try:
            xs = [float(v) for v in inp.X]
        except Exception:
            xs = []

        if len(xs) == 4:
            vals = [
                xs[1],   
                xs[2],   
                xs[3],   
                0.0,     
                xs[0],   
            ]
            return np.array([vals], dtype=float)
        elif len(xs) >= 5:
            vals = [
                xs[0],   
                xs[1],   
                xs[2],   
                xs[3],   
                xs[4],   
            ]
            return np.array([vals], dtype=float)

    src = dict(inp.features or {})  

    if inp.couponValue is not None:
        src["value"] = inp.couponValue
    if inp.acctAgeHours is not None:
        src["acctAgeHours"] = inp.acctAgeHours
    if inp.device_redemptions24h is not None:
        src["device24h"] = inp.device_redemptions24h
    if inp.ip_uniqueAccounts10m is not None:
        src["ip10m"] = inp.ip_uniqueAccounts10m
    if inp.user_redemptions24h is not None:
        src["user24h"] = inp.user_redemptions24h

    vals = [
        _as_float(src.get("acctAgeHours")),
        _as_float(src.get("device24h")),
        _as_float(src.get("ip10m")),
        _as_float(src.get("user24h")),
        _as_float(src.get("value")),
    ]
    return np.array([vals], dtype=float)

def _normalize_anomaly(raw: float) -> float:
    score = 1.0 - (raw + 0.5)
    return float(np.clip(score, 0.0, 1.0))

def _top_contributors(x: np.ndarray, k: int = 3) -> List[str]:
    diffs = np.abs(x[0] - _center)
    idx = np.argsort(diffs)[::-1][:k]
    return [_features_order[i] for i in idx]

def load_or_init():
    global _model
    try:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
            print("Model loaded from", MODEL_PATH)
    except Exception:
        print("Initializing new model…")
        _model = IsolationForest(
            n_estimators=IF_TREES,
            contamination=IF_CONTAM,
            random_state=42
        )
        X = np.random.normal(loc=_center, scale=[50, 1, 1, 1, 3], size=(200, 5))
        _model.fit(X)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(_model, f)
        print("Model initialized and saved to", MODEL_PATH)

# ---- Endpoints ----
@app.post("/score")
def score(inp: ScoreIn):
    global _model
    if _model is None:
        load_or_init()

    x = _extract_vector(inp)
    raw = float(_model.decision_function(x)[0])
    s = _normalize_anomaly(raw)
    top = _top_contributors(x)

    return {"score": round(s, 4), "top": top}

@app.post("/train")
def train(inp: TrainIn):
    global _model
    if inp.legit:
        X = [[_as_float(r.get(k)) for k in _features_order] for r in inp.legit]
        X = np.array(X, dtype=float)
    else:
        X = np.random.normal(loc=_center, scale=[50, 1, 1, 1, 3], size=(300, 5))

    _model = IsolationForest(
        n_estimators=max(50, IF_TREES),
        contamination=IF_CONTAM,
        random_state=42
    )
    _model.fit(X)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(_model, f)
    return {"ok": True, "trained_on": int(X.shape[0])}

@app.get("/health")
def health():
    return {"ok": True}


@app.get("/version")
def version():
    return {
        "ok": True,
        "port": PORT,
        "model_path": MODEL_PATH,
        "if_trees": IF_TREES,
        "if_contamination": IF_CONTAM,
        "features_order": _features_order,
    }

if __name__ == "__main__":
    load_or_init()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
