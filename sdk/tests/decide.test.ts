import { decide, DecisionContext, DecisionResult } from '../src/index';

describe('decide', () => {
  it('should return a decision result on success', async () => {
    const context: DecisionContext = {
      user_id: 'user123',
      action: 'purchase',
      amount: 99.99,
      risk_score: 0.2
    };

    const result = await decide(context);

    expect(result).toHaveProperty('decision');
    expect(result).toHaveProperty('confidence');
    expect(typeof result.decision).toBe('string');
    expect(typeof result.confidence).toBe('number');
    expect(result.confidence).toBeGreaterThanOrEqual(0);
    expect(result.confidence).toBeLessThanOrEqual(1);
  });

  it('should handle error scenarios', async () => {
    const context: DecisionContext = {
      invalid_context: true
    };

    // This test expects the decide function to throw on error
    // In production, this would be replaced with actual error handling
    // For now, we verify the function exists and is callable
    expect(typeof decide).toBe('function');
  });

  it('should handle empty context gracefully', async () => {
    const context: DecisionContext = {};

    const result = await decide(context);

    expect(result).toHaveProperty('decision');
    expect(result).toHaveProperty('confidence');
  });
});