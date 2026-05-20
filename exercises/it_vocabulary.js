const itVocabularyExercises = [
  {
    word: 'Algorithm',
    definition: 'A set of instructions designed to perform a specific task.',
    exercise: 'Fill in the blank: An ________ is a step-by-step procedure to solve a problem.',
    answer: 'algorithm'
  },
  {
    word: 'Debugging',
    definition: 'The process of finding and resolving defects or problems within a computer program that prevent correct operation.',
    exercise: 'What term describes the process of finding errors in software code?',
    answer: 'debugging'
  },
  {
    word: 'Encryption',
    definition: 'The process of converting information or data into a code, especially to prevent unauthorized access.',
    exercise: 'True or False: Encryption is used to make data more readable.',
    answer: 'False'
  }
];

function generateExercise() {
  const randomIndex = Math.floor(Math.random() * itVocabularyExercises.length);
  const exercise = itVocabularyExercises[randomIndex];
  console.log(`Word: ${exercise.word}`);
  console.log(`Definition: ${exercise.definition}`);
  console.log(`Exercise: ${exercise.exercise}`);
  return exercise.answer;
}

module.exports = { generateExercise };