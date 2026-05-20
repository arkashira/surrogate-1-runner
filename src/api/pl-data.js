import { fetchPLData } from '../services/plService';

export default async function handler(req, res) {
  const { range } = req.query;
  const data = await fetchPLData(range);
  res.status(200).json(data);
}