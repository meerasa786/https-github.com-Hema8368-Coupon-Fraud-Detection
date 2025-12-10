# Project Setup Guide

This project consists of three main components: a Backend API, Frontend Applications (Admin & Checkout), and an ML Service.

Follow the steps below to set up and run each component.

## 1. Backend API (`/api`)
This is the Node.js Express server.

### Setup
Navigate to the `api` directory and install dependencies:
```sh
cd api
npm install
```

### Run
Start the server:
```sh
node server.js
```
> Note: Ensure you have a `.env` file configured if required.

---

## 2. Frontend Applications (`/apps`)
There are two frontend applications: **Admin** and **Checkout**.

### Admin Panel
Navigate to the admin app directory:
```sh
cd apps/admin
npm install
npm run dev
```

### Checkout App
Navigate to the checkout app directory:
```sh
cd apps/checkout
npm install
npm run dev
```

---

## 3. ML Service (`/ml`)
This is the Python FastAPI machine learning service.

### Setup
Navigate to the `ml` directory and install dependencies:
```sh
cd ml
pip install -r requirements.txt
```

### Run
Start the FastAPI server:
```sh
python main.py
```
The service will start on port `8000`.

---

## Summary of Ports (Default)
- **API**: Check `server.js` or console logs (likely 3000 or 5000)
- **Frontend Apps**: Typically provided by Vite (e.g., `5173`)
- **ML Service**: `8000`