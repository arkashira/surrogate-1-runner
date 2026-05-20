const fs = require('fs');
const path = require('path');

class ImportVerifier {
  constructor(projectRoot) {
    this.projectRoot = projectRoot;
    this.packageJson = JSON.parse(fs.readFileSync(path.join(projectRoot, 'package.json'), 'utf8'));
  }

  verifyFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const imports = this.extractImports(content);
    const missingImports = this.checkMissingImports(imports);
    const incorrectImports = this.checkIncorrectImports(imports);
    const duplicateImports = this.checkDuplicateImports(imports);

    return {
      filePath,
      missingImports,
      incorrectImports,
      duplicateImports,
      hasIssues: missingImports.length > 0 || incorrectImports.length > 0 || duplicateImports.length > 0
    };
  }

  extractImports(content) {
    const importRegex = /import\s+(?:(?:[\w*{}\n, ]+) from\s+)?["']([^"']+)["']/g;
    const imports = [];
    let match;

    while ((match = importRegex.exec(content)) !== null) {
      imports.push(match[1]);
    }

    return imports;
  }

  checkMissingImports(imports) {
    const missing = [];
    const packageDependencies = Object.keys(this.packageJson.dependencies || {});

    imports.forEach(importPath => {
      if (!packageDependencies.includes(importPath)) {
        missing.push(importPath);
      }
    });

    return missing;
  }

  checkIncorrectImports(imports) {
    const incorrect = [];
    const packageDependencies = Object.keys(this.packageJson.dependencies || {});

    imports.forEach(importPath => {
      if (packageDependencies.includes(importPath)) {
        const packagePath = this.packageJson.dependencies[importPath];
        if (!fs.existsSync(path.join(this.projectRoot, 'node_modules', importPath, packagePath))) {
          incorrect.push(importPath);
        }
      }
    });

    return incorrect;
  }

  checkDuplicateImports(imports) {
    const duplicates = [];
    const seen = new Set();

    imports.forEach(importPath => {
      if (seen.has(importPath)) {
        duplicates.push(importPath);
      } else {
        seen.add(importPath);
      }
    });

    return duplicates;
  }
}

module.exports = ImportVerifier;