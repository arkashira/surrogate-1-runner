const fs = require('fs');
const path = require('path');

/**
 * Extracts all dependencies from package.json (including devDependencies).
 */
function getPackageJsonDependencies(packageJsonPath) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    return [
        ...Object.keys(packageJson.dependencies || {}),
        ...Object.keys(packageJson.devDependencies || {})
    ];
}

/**
 * Extracts all imports/require statements from a file.
 */
function extractImportsFromFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const importRegex = /(?:import\s+(?:[\w*{}\s,]+ from\s+)?['"]([^'"]+)['"]|require\(['"]([^'"]+)['"]\))/g;
    const imports = [];
    let match;

    while ((match = importRegex.exec(content)) !== null) {
        imports.push(match[1] || match[2]);
    }

    return imports;
}

/**
 * Recursively scans files in a directory to find imports not declared in package.json.
 */
function findMismatchedImports(directory, packageJsonPath) {
    const dependencies = getPackageJsonDependencies(packageJsonPath);
    const mismatches = [];

    fs.readdirSync(directory).forEach(file => {
        const filePath = path.join(directory, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            mismatches.push(...findMismatchedImports(filePath, packageJsonPath));
        } else if (filePath.endsWith('.js') || filePath.endsWith('.ts')) {
            const imports = extractImportsFromFile(filePath);
            imports.forEach(imported => {
                if (!dependencies.includes(imported)) {
                    mismatches.push({ file: filePath, import: imported });
                }
            });
        }
    });

    return mismatches;
}

module.exports = { findMismatchedImports };