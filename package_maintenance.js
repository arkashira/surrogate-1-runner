const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const readdir = promisify(fs.readdir);
const stat = promisify(fs.stat);

async function findImportsInFile(filePath) {
  const content = await fs.promises.readFile(filePath, 'utf8');
  const importRegex = /import\s+.*\s+from\s+['"]([^'"]+)['"]/g;
  let matches;
  const imports = new Set();
  
  while ((matches = importRegex.exec(content)) !== null) {
    const modulePath = matches[1];
    // Skip relative imports and built-in modules
    if (!modulePath.startsWith('.') && !modulePath.includes('/') && 
        !['react', 'node:'].includes(modulePath)) {
      imports.add(modulePath);
    }
  }
  return Array.from(imports);
}

async function scanDirectory(dirPath) {
  const entries = await readdir(dirPath);
  const files = [];
  
  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry);
    const stats = await stat(fullPath);
    
    if (stats.isDirectory()) {
      const subFiles = await scanDirectory(fullPath);
      files.push(...subFiles);
    } else if (stats.isFile() && 
              (entry.endsWith('.js') || entry.endsWith('.jsx') || 
               entry.endsWith('.ts') || entry.endsWith('.tsx'))) {
      files.push(fullPath);
    }
  }
  return files;
}

async function verifyPackageConsistency() {
  const projectRoot = path.resolve(__dirname, '..');
  const packageJsonPath = path.join(projectRoot, 'package.json');
  const packageJson = JSON.parse(await fs.promises.readFile(packageJsonPath, 'utf8'));
  
  const allDependencies = new Set([
    ...Object.keys(packageJson.dependencies || {}),
    ...Object.keys(packageJson.devDependencies || {})
  ]);
  
  const sourceFiles = await scanDirectory(path.join(projectRoot, 'src'));
  const testFiles = await scanDirectory(path.join(projectRoot, 'test'));
  
  const allFiles = [...sourceFiles, ...testFiles];
  const allImports = new Set();
  
  for (const file of allFiles) {
    const imports = await findImportsInFile(file);
    imports.forEach(pkg => allImports.add(pkg));
  }
  
  const missingInPackage = [];
  for (const imported of allImports) {
    if (!allDependencies.has(imported)) {
      missingInPackage.push(imported);
    }
  }
  
  if (missingInPackage.length > 0) {
    console.error(`❌ Missing dependencies in package.json: ${missingInPackage.join(', ')}`);
    console.error('Run: npm install <package-name> --save or --save-dev as appropriate');
    process.exit(1);
  }
  
  console.log('✅ All imports have corresponding package.json entries');
}

verifyPackageConsistency().catch(err => {
  console.error('Error during package verification:', err);
  process.exit(1);
});