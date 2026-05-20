import { GoogleAuth } from 'google-auth-library';
import fetch from 'node-fetch';
import { CloudBillingClient } from '@google-cloud/billing';
import { serviceAccount } from 'google-auth-library';

/**
 * Unified Cloud Cost Estimator API client.
 *
 * This module provides a thin wrapper around the Google Cloud Billing
 * Export API to retrieve a line‑item cost breakdown for a given GCP
 * project, as well as AWS and Azure cost breakdowns. It is deliberately
 * lightweight – it authenticates using Application Default Credentials
 * and issues simple REST requests to the Cloud Billing Budget service,
 * which returns cost data in a consumable JSON format.
 *
 * The function is designed for real‑time usage: callers can invoke it
 * repeatedly (e.g., via a polling loop or a WebSocket subscription) to
 * obtain up‑to‑date cost information as resources are created or
 * modified.
 *
 * @param projectId The GCP project identifier (e.g., "my-project").
 * @param start_time The start time for the cost breakdown (e.g., "2023-01-01").
 * @param end_time The end time for the cost breakdown (e.g., "2023-01-31").
 * @returns A promise that resolves to an array of cost line items.
 */
export async function fetchUnifiedCloudCostBreakdown(
  projectId: string,
  start_time: string,
  end_time: string,
): Promise<any[]> {
  // Acquire an auth client using ADC (Application Default Credentials).
  const auth = new GoogleAuth({
    scopes: ['https://www.googleapis.com/auth/cloud-billing.readonly'],
  });

  const client = await auth.getClient();

  // Construct the REST endpoint.  The Cloud Billing API does not expose a
  // direct "cost breakdown" endpoint, but the "services" and "sku" resources
  // can be queried via the Cloud Billing Catalog and usage export tables.
  // For the purpose of this integration we use the "costManagement" view
  // provided by the Cloud Billing Budget API, which returns aggregated
  // cost data per SKU.
  const url = `https://cloudbilling.googleapis.com/v1/projects/${projectId}/billingInfo`;

  // Perform the authenticated request.
  const res = await client.request({
    url,
    method: 'GET',
  });

  // The response shape varies; we normalise it to a simple array of line items.
  // If the API returns no data, return an empty array.
  if (!res || !res.data) {
    return [];
  }

  // Example normalisation – adapt as needed for downstream consumers.
  const lineItems = (res.data as any).costAmount ? [
    {
      description: 'Total Project Cost',
      amount: (res.data as any).costAmount,
      currency: (res.data as any).currencyCode || 'USD',
    },
  ] : [];

  // AWS and Azure cost breakdowns
  const awsEstimator = new AWSCostEstimator();
  const azureEstimator = new AzureCostEstimator();
  const awsCosts = await awsEstimator.getCostBreakdown(projectId, start_time, end_time);
  const azureCosts = await azureEstimator.getCostBreakdown(projectId, start_time, end_time);

  // Unified cost breakdown
  const unifiedCosts = {
    'gcp': lineItems,
    'aws': awsCosts,
    'azure': azureCosts,
  };

  return unifiedCosts;
}

/**
 * Helper used by the platform's real‑time updater.
 *
 * This function continuously polls the GCP cost endpoint at a configurable
 * interval and invokes a callback whenever the cost data changes.
 *
 * @param projectId GCP project identifier.
 * @param intervalMs Polling interval in milliseconds (default 30 000 ms).
 * @param onUpdate Callback invoked with the latest cost breakdown.
 */
export function startUnifiedCloudCostRealtimeWatcher(
  projectId: string,
  onUpdate: (costs: any[]) => void,
  intervalMs = 30_000,
): () => void {
  let previous: string | null = null;
  let stopped = false;

  const poll = async () => {
    if (stopped) return;
    try {
      const costs = await fetchUnifiedCloudCostBreakdown(projectId, '2023-01-01', '2023-01-31');
      const serialized = JSON.stringify(costs);
      if (serialized !== previous) {
        previous = serialized;
        onUpdate(costs);
      }
    } catch (err) {
      // Log but continue polling – real‑time UI can decide how to surface errors.
      console.error('Cloud cost fetch error:', err);
    } finally {
      setTimeout(poll, intervalMs);
    }
  };

  // Kick off the first poll.
  poll();

  // Return a stop function for callers to clean up.
  return () => {
    stopped = true;
  };
}