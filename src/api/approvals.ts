import type { NextApiRequest, NextApiResponse } from 'next';
import { Approval } from '../types';

export default function handler(req: NextApiRequest, res: NextApiResponse<Approval[]>) {
  const now = Date.now();
  const approvals: Approval[] = [
    {
      id: '1',
      message: 'Approval for project C',
      link: 'https://costinel.example.com/approvals/1',
      timestamp: new Date(now - 3600_000).toISOString(),
    },
    {
      id: '2',
      message: 'Approval for project D',
      link: 'https://costinel.example.com/approvals/2',
      timestamp: new Date(now - 7200_000).toISOString(),
    },
    {
      id: '3',
      message: 'Approval for project E',
      link: 'https://costinel.example.com/approvals/3',
      timestamp: new Date(now - 10_800_000).toISOString(),
    },
  ];
  res.status(200).json(approvals);
}