import { Step, StepResult } from '../models';

export async function executeStep(step: Step): Promise<StepResult> {
  // TODO: switch on step.type and call the appropriate handler
  // For now we simulate a successful step.
  return {
    stepId: step.id,
    status: 'completed',
    data: 'Sample data',
  };
}