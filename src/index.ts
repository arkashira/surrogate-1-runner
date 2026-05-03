import express from 'express';
import requestsRouter from './routes/requests';

const app = express();
app.use(express.json());

app.use('/requests', requestsRouter);

const PORT = Number(process.env.PORT) || 3000;
app.listen(PORT, () => {
  console.log(`Requests service listening on port ${PORT}`);
});