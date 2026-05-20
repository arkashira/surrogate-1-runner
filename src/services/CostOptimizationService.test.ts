import { CostOptimizationService } from './CostOptimizationService';
import { CostOptimizationClient } from 'costinel-api';

jest.mock('costinel-api');

describe('CostOptimizationService', () => {
  let service: CostOptimizationService;
  let mockClient: jest.Mocked<CostOptimizationClient>;

  beforeEach(() => {
    mockClient = new CostOptimizationClient() as jest.Mocked<CostOptimizationClient>;
    (CostOptimizationClient as jest.Mock).mockReturnValue(mockClient);
    service = new CostOptimizationService();
  });

  it('should set cost optimization policy', async () => {
    const policy = {};
    await service.setCostOptimizationPolicy(policy);
    expect(mockClient.setPolicy).toHaveBeenCalledWith(policy);
  });

  it('should enforce policies', async () => {
    await service.enforcePolicies();
    expect(mockClient.enforcePolicies).toHaveBeenCalled(); // Correct method name from Candidate 2
  });

  it('should report policy violations', async () => {
    const violations = [{ id: '1', message: 'Violation 1' }];
    mockClient.reportViolations.mockResolvedValue(violations); // Correct method name from Candidate 2
    const result = await service.reportViolations();
    expect(result).toEqual(violations);
  });
});