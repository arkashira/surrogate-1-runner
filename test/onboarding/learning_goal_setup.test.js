const { setLearningGoal, getLearningGoal } = require('../../onboarding/learning_goal_setup');
const fs = require('fs');
const path = require('path');

// Resolve the same data file used by the module.
const DATA_FILE = path.resolve(__dirname, '..', '..', 'data', 'learning_goals.json');

beforeEach(() => {
  // Ensure a clean state before each test.
  if (fs.existsSync(DATA_FILE)) {
    fs.unlinkSync(DATA_FILE);
  }
});

test('set and retrieve a learning goal', async () => {
  const userId = 'user-123';
  const goal = 'Master the fundamentals of JavaScript';

  const stored = await setLearningGoal(userId, goal);
  expect(stored).toMatchObject({ goal });

  const fetched = getLearningGoal(userId);
  expect(fetched).toMatchObject({ goal });
});

test('reject empty learning goal', async () => {
  await expect(setLearningGoal('user-456', '')).rejects.toThrow('Learning goal must be a non‑empty string');
});

test('reject overly long learning goal', async () => {
  const longGoal = 'a'.repeat(201);
  await expect(setLearningGoal('user-789', longGoal)).rejects.toThrow('Learning goal must be 200 characters or fewer');
});