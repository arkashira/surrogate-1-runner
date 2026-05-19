import { NextApiRequest, NextApiResponse } from 'next';
import { connectToDatabase } from '../../utils/mongodb';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const { db } = await connectToDatabase();
    const { name, email, feedback } = req.body;

    const result = await db.collection('feedback').insertOne({
      name,
      email,
      feedback,
      createdAt: new Date(),
    });

    res.status(200).json({ success: true, data: result });
  } catch (error) {
    console.error('Error saving feedback:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
}