import { decide as decideInternal } from './decision-service';

export interface DecisionContext {
  [key: string]: unknown;
}

export interface DecisionResult {
  decision: string;
  confidence: number;
  metadata?: Record<string, unknown>;
}

export async function decide(context: DecisionContext): Promise<DecisionResult> {
  try {
    const result = await decideInternal(context);
    return result;
  } catch (error) {
    throw new Error(`Decision failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}

export default decide;