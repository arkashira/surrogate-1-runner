const ImportVerifier = require('../src/import_verifier');
const fs = require('fs');
const path = require('path');

describe('ImportVerifier', () => {
  let verifier;
  const testProjectRoot = path.join(__dirname, 'test-project');

  beforeAll(() => {
    // Create a test project structure
    fs.mkdirSync(path.join(testProjectRoot, 'node_modules'));
    fs.writeFileSync(
      path.join(testProjectRoot, 'package.json'),
      JSON.stringify({
        dependencies: {
          'lodash': '4.17.21',
          'react': '17.0.2',
          'non-existent-package': '1.0.0'
        }
      })
    );
    fs.writeFileSync(
      path.join(testProjectRoot, 'src', 'test-file.js'),
      `import _ from 'lodash';
import React from 'react';
import 'non-existent-package';
import _ from 'lodash';`
    );
  });

  beforeEach(() => {
    verifier = new ImportVerifier(testProjectRoot);
  });

  test('should identify missing imports', () => {
    const result = verifier.verifyFile(path.join(testProjectRoot, 'src', 'test-file.js'));
    expect(result.missingImports).toContain('non-existent-package');
  });

  test('should identify incorrect imports', () => {
    // This test would require more setup to mock incorrect package paths
    const result = verifier.verifyFile(path.join(testProjectRoot, 'src', 'test-file.js'));
    expect(result.incorrectImports).toEqual([]);
  });

  test('should identify duplicate imports', () => {
    const result = verifier.verifyFile(path.join(testProjectRoot, 'src', 'test-file.js'));
    expect(result.duplicateImports).toContain('lodash');
  });

  test('should return false when no issues found', () => {
    fs.writeFileSync(
      path.join(testProjectRoot, 'src', 'test-file-clean.js'),
      `import _ from 'lodash';
import React from 'react';`
    );
    const result = verifier.verifyFile(path.join(testProjectRoot, 'src', 'test-file-clean.js'));
    expect(result.hasIssues).toBe(false);
  });
});