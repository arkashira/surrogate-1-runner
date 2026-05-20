const fs = require('fs');
const path = require('path');

function verifyImports(projectRoot) {
  const packageJsonPath = path.join(projectRoot, 'package.json');
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

  const importStatements = [];
  const files = fs.readdirSync(projectRoot);
  for (const file of files) {
    if (path.extname(file) === '.js') {
      const fileContent = fs.readFileSync(path.join(projectRoot, file), 'utf8');
      const matches = fileContent.match(/import\s+[^\s]+/g);
      if (matches) {
        importStatements.push(...matches.map(match => match.split(' ')[1]));
      }
    }
  }

  const missingImports = importStatements.filter(importName => !packageJson.dependencies[importName]);

  if (missingImports.length > 0) {
    console.error(`The following import statements have no corresponding entries in package.json: ${missingImports.join(', ')}`);
    process.exit(1);
  } else {
    console.log('All import statements have corresponding entries in package.json');
  }
}

verifyImports(__dirname);