const router = require('express').Router();
const Coupon = require('../../models/Coupon');
const CouponCode = require('../../models/CouponCode');

router.post('/apply-coupon', async (req, res) => {
  try {
    const { code, orderAmount } = req.body || {};
    if (!code || typeof orderAmount !== 'number') {
      return res.status(400).json({ ok: false, msg: 'code and orderAmount are required' });
    }

    let couponDoc = null;
    let singleUseMode = false;

    const cc = await CouponCode.findOne({ code }).populate('couponId').lean();
    if (cc && cc.couponId) {
      couponDoc = cc.couponId;
      singleUseMode = true;
      if (!couponDoc.singleUse) {
        return res.status(400).json({ ok: false, msg: 'This code is not valid for single-use mode' });
      }
      if (cc.usedBy) {
        return res.status(400).json({ ok: false, msg: 'Code already used' });
      }
    }

    if (!couponDoc) {
      couponDoc = await Coupon.findOne({ code }).lean();
      if (!couponDoc) {
        return res.status(404).json({ ok: false, msg: 'Coupon not found' });
      }
      singleUseMode = !!couponDoc.singleUse;
      if (singleUseMode) {
        return res.status(400).json({ ok: false, msg: 'Single-use code not recognized' });
      }
    }
    if (couponDoc.status !== 'active') {
      return res.status(400).json({ ok: false, msg: 'Coupon is not active' });
    }
    if (couponDoc.startAt && Date.now() < new Date(couponDoc.startAt).getTime()) {
      return res.status(400).json({ ok: false, msg: 'Coupon not started yet' });
    }
    if (couponDoc.endAt && Date.now() > new Date(couponDoc.endAt).getTime()) {
      return res.status(400).json({ ok: false, msg: 'Coupon expired' });
    }
    if (couponDoc.minOrder && orderAmount < couponDoc.minOrder) {
      return res.status(400).json({ ok: false, msg: `Minimum order must be ≥ ${couponDoc.minOrder}` });
    }

    let discount = 0;
    if (couponDoc.type === 'fixed') discount = couponDoc.value;
    if (couponDoc.type === 'percent') discount = +(orderAmount * (couponDoc.value / 100)).toFixed(2);
    const finalAmount = Math.max(0, +(orderAmount - discount).toFixed(2));

    return res.json({
      ok: true,
      couponId: couponDoc._id,
      singleUse: singleUseMode,
      discount,
      finalAmount
    });
  } catch (e) {
    console.error('[apply-coupon] error:', e);
    return res.status(500).json({ ok: false, msg: 'Internal error' });
  }
});

module.exports = router;
