import { EventEmitter } from 'node:events';
import { v4 as uuidv4 } from 'uuid';
import {
  CostExplorerClient,
  GetCostAndUsageCommand,
  GetCostAndUsageCommandInput,
  GetCostAndUsageCommandOutput,
} from '@aws-sdk/client-costexplorer';

/**
 * Represents a single line‑item of AWS cost data.
 */
export interface LineItem {
  /** Unique identifier for the line item */
  id: string;
  /** AWS service name (e.g., EC2, S3) */
  service: string;
  /** Usage type (e.g., BoxUsage, GB-Mo) */
  usageType: string;
  /** Cost in USD */
  cost: number;
  /** Timestamp for the data point */
  timestamp: string;
}

/**
 * Options for configuring the real‑time cost pipeline.
 */
export interface RealTimeCostPipelineOptions {
  /** Polling interval in milliseconds (default: 60_000 ms). */
  intervalMs?: number;
  /** AWS Cost Explorer client instance. */
  client?: CostExplorerClient;
  /** Time window in hours to look back (default: 24). */
  lookbackHours?: number;
}

/**
 * Real‑time cost data pipeline.
 *
 * The pipeline periodically queries AWS Cost Explorer for recent cost data,
 * transforms the response into a list of {@link LineItem}s, and emits a `data` event.
 * It uses HOURLY granularity to provide the finest resolution available via API.
 */
export class RealTimeCostPipeline extends EventEmitter {
  private readonly intervalMs: number;
  private readonly client: CostExplorerClient;
  private readonly lookbackHours: number;
  private intervalHandle?: NodeJS.Timeout;

  constructor(options: RealTimeCostPipelineOptions = {}) {
    super();
    this.intervalMs = options.intervalMs ?? 60_000; // default 1 minute
    this.lookbackHours = options.lookbackHours ?? 24; // default 24 hours to ensure data availability
    this.client = options.client ?? new CostExplorerClient({});
  }

  /**
   * Starts the polling loop.
   */
  public start(): void {
    if (this.intervalHandle) {
      return; // already running
    }
    this.fetchAndEmit(); // immediate first fetch
    this.intervalHandle = setInterval(() => this.fetchAndEmit(), this.intervalMs);
  }

  /**
   * Stops the polling loop.
   */
  public stop(): void {
    if (this.intervalHandle) {
      clearInterval(this.intervalHandle);
      this.intervalHandle = undefined;
    }
  }

  /**
   * Fetches cost data and emits it.
   */
  private async fetchAndEmit(): Promise<void> {
    try {
      const lineItems = await this.fetchCostData();
      this.emit('data', lineItems);
    } catch (err) {
      this.emit('error', err);
    }
  }

  /**
   * Calls AWS Cost Explorer to retrieve cost data.
   * Uses HOURLY granularity for better resolution.
   */
  private async fetchCostData(): Promise<LineItem[]> {
    const now = new Date();
    const startDate = new Date(now.getTime() - this.lookbackHours * 60 * 60 * 1000);

    const input: GetCostAndUsageCommandInput = {
      TimePeriod: {
        Start: startDate.toISOString().split('T')[0], // YYYY-MM-DD
        End: now.toISOString().split('T')[0],         // YYYY-MM-DD
      },
      Granularity: 'HOURLY', // Corrected to HOURLY for recent data
      Metrics: ['UnblendedCost'],
      GroupBy: [
        { Type: 'DIMENSION', Key: 'SERVICE' },
        { Type: 'DIMENSION', Key: 'USAGE_TYPE' },
      ],
    };

    const command = new GetCostAndUsageCommand(input);
    
    let response: GetCostAndUsageCommandOutput;
    try {
      response = await this.client.send(command);
    } catch (error) {
      // Re-throw to be caught by fetchAndEmit
      throw new Error(`AWS Cost Explorer API failed: ${error}`);
    }

    if (!response.ResultsByTime || response.ResultsByTime.length === 0) {
      return [];
    }

    const lineItems: LineItem[] = [];

    // Iterate through time periods (hours)
    for (const result of response.ResultsByTime) {
      const groups = result.Groups ?? [];
      const timeStamp = result.TimePeriod?.Start ?? new Date().toISOString();

      for (const group of groups) {
        const service = group.Keys?.[0] ?? 'UnknownService';
        const usageType = group.Keys?.[1] ?? 'UnknownUsage';
        
        // Safely parse cost, default to 0
        const cost = Number(group.Metrics?.UnblendedCost?.Amount ?? '0') || 0;

        if (cost > 0) { // Optional: Filter out zero-cost items to reduce noise
            lineItems.push({
            id: uuidv4(),
            service,
            usageType,
            cost,
            timestamp: timeStamp,
            });
        }
      }
    }

    return lineItems;
  }
}