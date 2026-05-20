import { analyzeAudioGain } from '../AudioGainControlAnalyzer';

test('optimizes when gain is within the optimal range', () => {
  const result = analyzeAudioGain(0.5);
  expect(result.optimized).toBe(true);
  expect(result.message).toBe('Audio gain is within the optimal range.');
});

test('detects low gain and returns corrective instruction', () => {
  const result = analyzeAudioGain(0.1);
  expect(result.optimized).toBe(false);
  expect(result.message).toMatch(/too low/);
});

test('detects high gain and returns corrective instruction', () => {
  const result = analyzeAudioGain(0.9);
  expect(result.optimized).toBe(false);
  expect(result.message).toMatch(/too high/);
});