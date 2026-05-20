const fs = require('fs-extra');
const path = require('path');

// Load the list of IT-related words (500+ entries)
const WORDS_PATH = path.join(__dirname, 'data', 'it_words.json');
const WORDS = fs.readJsonSync(WORDS_PATH);

// Simple persistent store for user progress
const PROGRESS_PATH = path.join(__dirname, 'data', 'progress.json');
let PROGRESS_STORE = {};
try {
  PROGRESS_STORE = fs.readJsonSync(PROGRESS_PATH);
} catch (_) {
  PROGRESS_STORE = {};
}

/**
 * Persist the in-memory progress store to disk.
 */
async function saveProgressStore() {
  await fs.writeJson(PROGRESS_PATH, PROGRESS_STORE, { spaces: 2 });
}

/**
 * Shuffle an array in-place using Fisher–Yates.
 */
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

/**
 * Generate a single multiple-choice question.
 * @param {string} correctWord
 * @returns {{question:string, options:string[]}}
 */
function makeQuestion(correctWord) {
  const options = new Set([correctWord]);
  while (options.size < 4) {
    const candidate = WORDS[Math.floor(Math.random() * WORDS.length)];
    options.add(candidate);
  }
  const optsArray = Array.from(options);
  return { question: `What is the meaning of "${correctWord}"?`, options: shuffle(optsArray) };
}

/**
 * VocabularyQuiz class encapsulates quiz generation and progress tracking.
 */
class VocabularyQuiz {
  /**
   * @param {string} userId – unique identifier for the user (e.g., email or UUID)
   */
  constructor(userId) {
    this.userId = userId;
    if (!PROGRESS_STORE[userId]) {
      PROGRESS_STORE[userId] = {
        totalQuizzes: 0,
        totalCorrect: 0,
        history: [] // { timestamp, score, total }
      };
      saveProgressStore();
    }
  }

  /**
   * Retrieve the current progress for the user.
   * @returns {{totalQuizzes:number,totalCorrect:number,history:Array}}
   */
  getProgress() {
    return PROGRESS_STORE[this.userId];
  }

  /**
   * Generate a quiz consisting of `numQuestions` multiple-choice items.
   * @param {number} [numQuestions=10]
   * @returns {Array<{question:string,options:string[]}>}
   */
  async generateQuiz(numQuestions = 10) {
    const selected = new Set();
    const quiz = [];

    while (quiz.length < numQuestions && selected.size < WORDS.length) {
      const word = WORDS[Math.floor(Math.random() * WORDS.length)];
      if (selected.has(word)) continue;
      selected.add(word);
      quiz.push(makeQuestion(word));
    }

    // Store the correct answers for later validation
    this._currentAnswers = Array.from(selected);
    return quiz;
  }

  /**
   * Evaluate a set of user answers.
   * @param {Array<string>} answers – user-selected option for each question, in order.
   * @returns {{score:number,total:number,details:Array<{question:string,correct:string,chosen:string,correctlyAnswered:boolean}>}}
   */
  submitAnswers(answers) {
    if (!this._currentAnswers) {
      throw new Error('No active quiz. Call generateQuiz() first.');
    }
    const total = this._currentAnswers.length;
    const details = [];
    let score = 0;

    for (let i = 0; i < total; i++) {
      const correct = this._currentAnswers[i];
      const chosen = answers[i];
      const correctlyAnswered = correct === chosen;
      if (correctlyAnswered) score += 1;
      details.push({
        question: `What is the meaning of "${correct}"?`,
        correct,
        chosen,
        correctlyAnswered,
      });
    }

    // Update progress
    const userProgress = PROGRESS_STORE[this.userId];
    userProgress.totalQuizzes += 1;
    userProgress.totalCorrect += score;
    userProgress.history.push({
      timestamp: new Date().toISOString(),
      score,
      total,
    });
    saveProgressStore();

    // Clean up current quiz state
    delete this._currentAnswers;

    return { score, total, details };
  }

  /**
   * Provide the full list of IT-related words (read-only).
   * @returns {Array<string>}
   */
  static getWordList() {
    return [...WORDS];
  }
}

module.exports = VocabularyQuiz;