const express = require('express');
const cors = require('cors');
require('dotenv').config();
const { connectMongo } = require('./db/mongo');

const app = express();


const checkoutOrigin = process.env.CHECKOUT_ORIGIN;
const adminOrigin = process.env.ADMIN_ORIGIN;
app.use(cors({}));

app.use(express.json({ limit: '1mb' }));

// health
app.get('/health', (req, res) => res.json({ ok: true }));

app.use('/api/public/auth', require('./routes/public/auth'));
app.use('/api/public', require('./routes/public'));

app.use('/api/admin/auth', require('./routes/admin/auth'));

app.use('/api/admin', require('./routes/admin'));

const PORT = process.env.PORT || 4000;
connectMongo().then(()=>{
  app.listen(PORT, () => console.log(`API up on :${PORT}`));
}).catch(err=>{
  console.error('Mongo connect failed:', err);
  process.exit(1);
});
