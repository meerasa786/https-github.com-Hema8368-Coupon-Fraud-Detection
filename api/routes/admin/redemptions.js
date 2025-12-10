const router = require('express').Router();
const Redemption = require('../../models/Redemption');

router.get('/', async (req, res) => {
  try {
    const { decision, couponCode, from, to, limit } = req.query;
    const q = {};

    if (decision) q.decision = decision;
    if (couponCode) q.couponCode = couponCode;
    
    if (from || to) {
      q.createdAt = {};
      if (from) q.createdAt.$gte = new Date(from);
      if (to) q.createdAt.$lte = new Date(to);
    }

    const limitNum = Math.min(Number(limit) || 100, 500);

    const rows = await Redemption.find(q)
      .sort({ createdAt: -1 })
      .limit(limitNum)
      .lean();

    return res.json({ ok: true, rows });
  } catch (e) {
    console.error('[admin/redemptions] error:', e);
    return res.status(500).json({ ok: false, msg: 'Failed to load redemptions' });
  }
});

module.exports = router;