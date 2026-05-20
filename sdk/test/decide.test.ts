import { decide } from '../src/decide';
import { expect } from 'chai';
import sinon from 'sinon';

describe('decide', () => {
  it('should return a JSON decision for valid input', async () => {
    const context = { key: 'value' };
    const expectedDecision = { action: 'approve' };

    // Mock the underlying decision-making logic
    const mockDecisionMaker = sinon.stub().resolves(expectedDecision);
    (decide as any).decisionMaker = mockDecisionMaker;

    const result = await decide(context);

    expect(result).to.deep.equal(expectedDecision);
    expect(mockDecisionMaker.calledWith(context)).to.be.true;
  });

  it('should handle errors gracefully', async () => {
    const context = { key: 'value' };

    // Mock the underlying decision-making logic to throw an error
    const mockDecisionMaker = sinon.stub().rejects(new Error('Something went wrong'));
    (decide as any).decisionMaker = mockDecisionMaker;

    try {
      await decide(context);
      expect.fail('Expected an error to be thrown');
    } catch (error) {
      expect(error.message).to.equal('Something went wrong');
    }
  });
});