import express from 'express';
import dashboardRoutes from './routes/dashboardRoutes';

const app = express();
app.use(express.json());

app.use('/api', dashboardRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

export default app;