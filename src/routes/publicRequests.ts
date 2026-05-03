import { Router, Request, Response } from 'express';
import { RequestPublicDto } from '../dtos/requestPublicDto';
import { RequestService } from '../services/requestService';

const router = Router();
const requestService = new RequestService();

router.get('/public/requests/:publicId', async (req: Request, res: Response) => {
  try {
    const publicId = req.params.publicId;
    const request = await requestService.getRequestByPublicId(publicId);
    if (!request) {
      return res.status(404).send('Request not found');
    }
    const requestPublicDto = new RequestPublicDto(
      request.title,
      request.status,
      request.timeline,
      request.sla,
      request.lastUpdated,
      getRequestStatusLabel(request.status)
    );
    return res.json(requestPublicDto);
  } catch (error) {
    console.error(error);
    return res.status(500).send('Internal Server Error');
  }
});

function getRequestStatusLabel(status: string): string {
  switch (status) {
    case 'pending':
      return 'Pending';
    case 'in_progress':
      return 'In Progress';
    case 'completed':
      return 'Completed';
    default:
      return 'Unknown';
  }
}

export default router;