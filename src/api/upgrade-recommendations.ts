import { NextApiRequest, NextApiResponse } from 'next';
import { UpgradeRecommendation } from '../types/UpgradeRecommendation';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { cpu, gpu, ram, budget } = req.body;

  // Mock data for recommendations
  const recommendations: UpgradeRecommendation[] = [
    {
      componentNames: ['Intel Core i7-12700K', 'NVIDIA RTX 3080', '32GB DDR4'],
      price: 1200,
      expectedFPS: 120,
      roi: 1.5,
    },
    {
      componentNames: ['AMD Ryzen 7 5800X', 'NVIDIA RTX 3070', '32GB DDR4'],
      price: 1000,
      expectedFPS: 110,
      roi: 1.3,
    },
    {
      componentNames: ['Intel Core i5-12600K', 'NVIDIA RTX 3060', '16GB DDR4'],
      price: 800,
      expectedFPS: 90,
      roi: 1.1,
    },
  ];

  res.status(200).json({ recommendations });
}