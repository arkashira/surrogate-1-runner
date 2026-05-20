/**
 * Jest tests for the persist utility.
 *
 * These tests verify that state can be saved, loaded, and cleared,
 * and that missing files are handled gracefully.
 */

const fs = require('fs').promises;
const path = require('path');
const os = require('os');

const {
  saveState,
  loadState,
  clearState,
  _internal: { getStateFilePath },
} = require('../persist');

describe('persist utility', () => {
  const testState = { step: 2, source: 'reddit', format: 'json' };
  const stateFile = getStateFilePath();

  afterAll(async () => {
    // Ensure cleanup even if a test fails.
    try {
      await fs.unlink(stateFile);
    } catch (_) {
      // ignore
    }
  });

  test('saveState writes a JSON file', async () => {
    await saveState(testState);
    const raw = await fs.readFile(stateFile, { encoding: 'utf8' });
    expect(JSON.parse(raw)).toEqual(testState);
  });

  test('loadState returns the saved object', async () => {
    // Ensure the file exists from previous test or write it again.
    await saveState(testState);
    const loaded = await loadState();
    expect(loaded).toEqual(testState);
  });

  test('loadState returns null when no file exists', async () => {
    await clearState(); // ensure file is removed
    const loaded = await loadState();
    expect(loaded).toBeNull();
  });

  test('clearState removes the file without error', async () => {
    await saveState(testState);
    await clearState();
    await expect(fs.access(stateFile)).rejects.toThrow();
  });

  test('saveState throws on invalid input', async () => {
    await expect(saveState(null)).rejects.toThrow(TypeError);
    await expect(saveState('string')).rejects.toThrow(TypeError);
  });
});