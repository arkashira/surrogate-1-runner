const express = require('express');
const app = express();
const specEditorRoutes = require('./routes/specEditorRoutes');

app.use(express.json());
app.use('/api', specEditorRoutes);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});