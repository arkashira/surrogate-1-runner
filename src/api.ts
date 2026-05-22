import express, { Request, Response } from 'express';
import { FeeService, FeeBreakdown, CloudProvider, ResourceFeeItem } from './services/feeService';

const app = express();
const feeService = new FeeService();

app.use(express.json());

/**
 * GET /api/fees/:provider
 * Retrieve real-time fee breakdown for a specific cloud provider
 *
 * @param provider - Cloud provider: 'aws' | 'azure' | 'gcp'
 * @returns Line-item fee breakdown with usage and cost details
 */
app.get('/api/fees/:provider', async (req: Request, res: Response): Promise<void> => {
  try {
    const { provider } = req.params;
    const validProviders: CloudProvider[] = ['aws', 'azure', 'gcp'];

    if (!validProviders.includes(provider)) {
      res.status(400).json({
        error: 'Invalid provider',
        message: `Provider must be one of: ${validProviders.join(', ')}`,
      });
      return;
    }

    const breakdown = await feeService.getFeeBreakdown(provider);
    res.json({
      provider,
      timestamp: new Date().toISOString(),
      breakdown,
    });
  } catch (error) {
    res.status(500).json({
      error: 'Failed to retrieve fee breakdown',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

/**
 * GET /api/fees
 * Retrieve real-time fee breakdown for all cloud providers
 *
 * @returns Combined fee breakdown for AWS, Azure, and GCP
 */
app.get('/api/fees', async (_req: Request, res: Response): Promise<void> => {
  try {
    const providers: CloudProvider[] = ['aws', 'azure', 'gcp'];
    const results = await Promise.all(
      providers.map(async (provider) => ({
        provider,
        breakdown: await feeService.getFeeBreakdown(provider),
      }))
    );

    const combined = results.reduce(
      (acc, { provider, breakdown }) => ({
        ...acc,
        [provider]: breakdown,
      }),
      {} as Record<CloudProvider, FeeBreakdown>
    );

    res.json({
      timestamp: new Date().toISOString(),
      providers: combined,
    });
  } catch (error) {
    res.status(500).json({
      error: 'Failed to retrieve fee breakdown',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

/**
 * GET /api/fees/:provider/resources/:resourceId
 * Retrieve detailed fee breakdown for a specific resource
 *
 * @param provider - Cloud provider: 'aws' | 'azure' | 'gcp'
 * @param resourceId - Specific resource identifier
 * @returns Detailed line-item fees for the resource
 */
app.get('/api/fees/:provider/resources/:resourceId', async (req: Request, res: Response): Promise<void> => {
  try {
    const { provider, resourceId } = req.params;
    const validProviders: CloudProvider[] = ['aws', 'azure', 'gcp'];

    if (!validProviders.includes(provider)) {
      res.status(400).json({
        error: 'Invalid provider',
        message: `Provider must be one of: ${validProviders.join(', ')}`,
      });
      return;
    }

    const breakdown = await feeService.getResourceFeeBreakdown(
      provider as CloudProvider,
      resourceId
    );

    res.json({
      provider,
      resourceId,
      timestamp: new Date().toISOString(),
      breakdown,
    });
  } catch (error) {
    res.status(500).json({
      error: 'Failed to retrieve resource fee breakdown',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Fee API server running on port ${PORT}`);
});

export default app;

// src/services/feeService.ts
import { FeeBreakdown, FeeLineItem, CloudProvider, ResourceFeeItem } from '../types';

export type CloudProvider = 'aws' | 'azure' | 'gcp';

/**
 * Service for retrieving real-time fee breakdowns from cloud providers
 */
export class FeeService {
  /**
   * Get real-time fee breakdown for a cloud provider
   */
  async getFeeBreakdown(provider: CloudProvider): Promise<FeeBreakdown> {
    switch (provider) {
      case 'aws':
        return this.getAWSFees();
      case 'azure':
        return this.getAzureFees();
      case 'gcp':
        return this.getGCPFees();
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
  }

  /**
   * Get detailed fee breakdown for a specific resource
   */
  async getResourceFeeBreakdown(
    provider: CloudProvider,
    resourceId: string
  ): Promise<ResourceFeeItem[]> {
    const breakdown = await this.getFeeBreakdown(provider);
    return breakdown.lineItems.filter((item) => item.resourceId === resourceId);
  }

  private async getAWSFees(): Promise<FeeBreakdown> {
    // Simulated real-time AWS cost data
    // In production, this would call AWS Cost Explorer API
    const lineItems: FeeLineItem[] = [
      // (...) Add the AWS fee breakdown data here
    ];

    // (...) Add the rest of the AWS fee breakdown implementation here
  }

  private async getAzureFees(): Promise<FeeBreakdown> {
    // Simulated real-time Azure cost data
    // In production, this would call Azure Cost Management API
    const lineItems: FeeLineItem[] = [
      // (...) Add the Azure fee breakdown data here
    ];

    // (...) Add the rest of the Azure fee breakdown implementation here
  }

  private async getGCPFees(): Promise<FeeBreakdown> {
    // Simulated real-time GCP cost data
    // In production, this would call Google Cloud Billing API
    const lineItems: FeeLineItem[] = [
      // (...) Add the GCP fee breakdown data here
    ];

    // (...) Add the rest of the GCP fee breakdown implementation here
  }
}