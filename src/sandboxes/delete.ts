import { Request, Response } from 'express';
import { deleteSandbox } from '../services/sandboxes';

const deleteSandboxApi = async (req: Request, res: Response): Promise<void> => {
  try {
    const { sandboxId } = req.params;

    if (!sandboxId) {
      res.status(400).json({ error: 'Sandbox ID is required' });
      return;
    }

    await deleteSandbox(sandboxId);
    res.status(204).send();
  } catch (error) {
    console.error('Error deleting sandbox:', error);
    res.status(500).json({ error: 'Failed to delete sandbox' });
  }
};

export default deleteSandboxApi;