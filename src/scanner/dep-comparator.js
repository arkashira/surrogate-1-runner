const fs = require('fs');
const path = require('path');
const glob = require('glob');
const { parse } = require('@babel/parser');
const traverse = require('@babel/traverse').default;

function readPackageJson() {
  const pkgPath = path.join(process.cwd(), 'package.json');
  return JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
}

function scanFilesForImports(dir) {
  const files = glob.sync(`${dir}/**/*.@(js|ts)`);
  const imports = [];

  files.forEach(file => {
    const content = fs.readFileSync(file, 'utf-8');
    const ast = parse(content, { sourceType: 'module', plugins: ['typescript'] });

    traverse(ast, {
      ImportDeclaration(path) {
        const source = path.node.source.value;
        imports.push({ file, source });
      }
    });
  });

  return imports;
}

function compareDependencies(imports, pkgJson) {
  const discrepancies = [];
  const dependencies = { ...pkgJson.dependencies, ...pkgJson.devDependencies };

  imports.forEach(importInfo => {
    const { file, source } = importInfo;
    if (!dependencies[source]) {
      discrepancies.push({ file, source, lineNumber: findLineNumber(file, source) });
    }
  });

  return discrepancies;
}

function findLineNumber(file, source) {
  const content = fs.readFileSync(file, 'utf-8');
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes(`import ${source}`)) {
      return i + 1;
    }
  }

  return -1;
}

function main() {
  const pkgJson = readPackageJson();
  const imports = scanFilesForImports('.');
  const discrepancies = compareDependencies(imports, pkgJson);

  if (discrepancies.length > 0) {
    console.log('Discrepancies found:');
    discrepancies.forEach(discrepancy => {
      console.log(`File: ${discrepancy.file}, Line: ${discrepancy.lineNumber}, Missing Dependency: ${discrepancy.source}`);
    });
  } else {
    console.log('No discrepancies found.');
  }
}

main();