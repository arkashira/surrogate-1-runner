const ProgressTracker = require('./tracking');

describe('ProgressTracker', () => {
  it('should track progress', () => {
    const tracker = new ProgressTracker();
    tracker.trackProgress('English', 'Grammar', 80);
    tracker.trackProgress('English', 'Vocabulary', 90);
    expect(tracker.getProgress('English')).toEqual({
      Grammar: 80,
      Vocabulary: 90
    });
  });

  it('should get all progress', () => {
    const tracker = new ProgressTracker();
    tracker.trackProgress('English', 'Grammar', 80);
    tracker.trackProgress('Spanish', 'Vocabulary', 90);
    expect(tracker.getAllProgress()).toEqual({
      English: {
        Grammar: 80
      },
      Spanish: {
        Vocabulary: 90
      }
    });
  });

  it('should visualize progress', () => {
    const tracker = new ProgressTracker();
    tracker.trackProgress('English', 'Grammar', 80);
    tracker.trackProgress('English', 'Vocabulary', 90);
    const progress = tracker.visualizeProgress('English');
    expect(progress.topics).toEqual(['Grammar', 'Vocabulary']);
    expect(progress.scores).toEqual([80, 90]);
    expect(progress.averageScore).toBe(85);
  });
});