/**
 * @jest-environment jsdom
 */

import { getProgress, recordAnswer, resetProgress } from '../progress';

describe('progress tracking', () => {
  const quizId = 'test-quiz';

  beforeEach(() => {
    localStorage.clear();
  });

  test('initial progress is zero', () => {
    const p = getProgress(quizId);
    expect(p).toEqual({ correct: 0, total: 0 });
  });

  test('recording correct answer updates progress', () => {
    recordAnswer(quizId, true);
    const p = getProgress(quizId);
    expect(p).toEqual({ correct: 1, total: 1 });
  });

  test('recording incorrect answer updates total only', () => {
    recordAnswer(quizId, false);
    const p = getProgress(quizId);
    expect(p).toEqual({ correct: 0, total: 1 });
  });

  test('multiple answers accumulate correctly', () => {
    recordAnswer(quizId, true);
    recordAnswer(quizId, false);
    recordAnswer(quizId, true);
    const p = getProgress(quizId);
    expect(p).toEqual({ correct: 2, total: 3 });
  });

  test('reset clears progress', () => {
    recordAnswer(quizId, true);
    resetProgress(quizId);
    const p = getProgress(quizId);
    expect(p).toEqual({ correct: 0, total: 0 });
  });
});