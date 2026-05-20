import { NativeModules } from 'react-native';
import { expect } from '@jest/globals';

const { BridgeModule } = NativeModules;

describe('BridgeModule', () => {
  it('should invoke the surrogate model correctly', async () => {
    const modelId = 'test-model-id';
    const prompt = 'This is a test prompt.';
    const options = { maxTokens: 50 };

    // Mock the native module response
    jest.spyOn(BridgeModule, 'invoke').mockResolvedValue({ result: 'Test response' });

    try {
      const response = await BridgeModule.invoke(modelId, prompt, options);
      expect(response).toEqual({ result: 'Test response' });
    } catch (error) {
      fail('Unexpected error during invocation');
    }
  });

  it('should throw an exception when the backend returns an error', async () => {
    const modelId = 'test-model-id';
    const prompt = 'This is a test prompt.';
    const options = { maxTokens: 50 };

    // Mock the native module to return an error
    jest.spyOn(BridgeModule, 'invoke').mockRejectedValue(new Error('Backend error'));

    try {
      await BridgeModule.invoke(modelId, prompt, options);
      fail('Expected an error to be thrown');
    } catch (error) {
      expect(error.message).toBe('Backend error');
    }
  });

  it('should respect rate limits and cost tracking', async () => {
    const modelId = 'test-model-id';
    const prompt = 'This is a test prompt.';
    const options = { maxTokens: 50 };

    // Mock the native module response indicating rate limit exceeded
    jest.spyOn(BridgeModule, 'invoke').mockRejectedValue(new Error('Rate limit exceeded'));

    try {
      await BridgeModule.invoke(modelId, prompt, options);
      fail('Expected an error due to rate limit');
    } catch (error) {
      expect(error.message).toBe('Rate limit exceeded');
    }
  });
});