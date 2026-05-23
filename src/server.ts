import express from 'express';
import templatesRouter from './api/templates';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use('/api/templates', templatesRouter);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});