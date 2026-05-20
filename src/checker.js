const fs = require('fs');
const path = require('path');
const glob = require('glob');
const { parse } = require('@babel/parser');
const traverse = require('@babel/traverse').default;

function readPackageJson() {
  const packageJsonPath = path.join(__dirname, '../package.json');
  return JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
}

function getDeclaredPackages(packageJson) {
  return new Set([
    ...Object.keys(packageJson.dependencies || {}),
    ...Object.keys(packageJson.devDependencies || {})
  ]);
}

function findImportsInFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const ast = parse(content, { sourceType: 'module' });
  const imports = [];

  traverse(ast, {
    ImportDeclaration(path) {
      const source = path.node.source.value;
      imports.push(source);
    }
  });

  return imports;
}

function resolvePackageNames(imports) {
  const packageNames = new Set();
  imports.forEach(importPath => {
    try {
      const resolvedPath = require.resolve(importPath, { paths: [__dirname] });
      const packageName = require(resolvedPath).name;
      packageNames.add(packageName);
    } catch (error) {
      // Ignore errors, it might be a local file import
    }
  });
  return packageNames;
}

function checkMissingImports() {
  const packageJson = readPackageJson();
  const declaredPackages = getDeclaredPackages(packageJson);

  const jsTsFiles = glob.sync('src/**/*.@(js|ts)');
  const allImports = jsTsFiles.flatMap(findImportsInFile);
  const importedPackages = resolvePackageNames(allImports);

  const missingImports = Array.from(importedPackages).filter(pkg => !declaredPackages.has(pkg));
  const result = {
    missingImports,
    hasErrors: missingImports.length > 0
  };

  console.log(JSON.stringify(result, null, 2));

  if (result.hasErrors) {
    process.exit(1);
  }
}

checkMissingImports();