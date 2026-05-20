import type { NextApiRequest, NextApiResponse } from 'next';
import { Alert } from '../types';

export default function handler(req: NextApiRequest, res: NextApiResponse<Alert[]>) {
  const now = Date.now();
  const alerts: Alert[] = [
    {
      id: '1',
      message: 'High spending detected in project A',
      link: 'https://costinel.example.com/alerts/1',
      timestamp: new Date(now - 3600_000).toISOString(),
    },
    {
      id: '2',
      message: 'Budget threshold reached for project B',
      link: 'https://costinel.example.com/alerts/2',
      timestamp: new Date(now - 7200_000).toISOString(),
    },
    {
      id: '3',
      message: 'Unusual spending pattern detected',
      link: 'https://costinel.example.com/alerts/3',
      timestamp: new Date(now - 10_800_000).toISOString(),
    },
  ];
  res.status(200).json(alerts);
}