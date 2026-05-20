const express = require('express');
const router = express.Router();

const validateQuantity = (req, res, next) => {
  const { quantity, minStockLevel, maxStockCapacity } = req.body;
  if (quantity < minStockLevel) {
    res.status(422).send({ error: 'Quantity is below minimum stock level' });
  } else if (quantity > maxStockCapacity) {
    res.status(422).send({ error: 'Quantity exceeds maximum stock capacity' });
  } else {
    next();
  }
};

router.use(validateQuantity);

module.exports = router;