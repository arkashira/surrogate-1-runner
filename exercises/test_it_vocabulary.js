const { generateExercise } = require('./it_vocabulary');

describe('IT Vocabulary Exercises', () => {
  it('should generate a valid exercise', () => {
    const answer = generateExercise();
    expect(typeof answer).toBe('string');
    expect(answer.length > 0).toBe(true);
  });
});