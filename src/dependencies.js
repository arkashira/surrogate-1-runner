import fs from 'fs/promises';
import path from 'path';
import { parseImports } from './parser.js';

/**
 * Identifies dependencies in a JavaScript/TypeScript file
 * @param {string} filePath - Path to the file to analyze
 * @returns {Promise<Array<string>>} Array of dependency module names
 */
export async function getDependencies(filePath) {
  try {
    const code = await fs.readFile(filePath, 'utf-8');
    const imports = parseImports(code);
    return [...new Set(imports.map(imp => imp.source))];
  } catch (error) {
    console.error(`Error processing file ${filePath}:`, error);
    return [];
  }
}

/**
 * Recursively scans a directory for dependencies
 * @param {string} directoryPath - Directory to scan
 * @param {Object} [options] - Configuration options
 * @param {Array<string>} [options.extensions] - File extensions to include
 * @returns {Promise<Map<string, Set<string>>>} Map of file paths to their dependencies
 */
export async function scanDirectory(directoryPath, options = {}) {
  const {
    extensions = ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs']
  } = options;

  const dependencies = new Map();
  const filesToProcess = [];

  async function walkDirectory(currentPath) {
    const entries = await fs.readdir(currentPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);

      if (entry.isDirectory()) {
        await walkDirectory(fullPath);
      } else if (entry.isFile() && extensions.some(ext => entry.name.endsWith(ext))) {
        filesToProcess.push(fullPath);
      }
    }
  }

  try {
    await walkDirectory(directoryPath);

    for (const filePath of filesToProcess) {
      try {
        const deps = await getDependencies(filePath);
        dependencies.set(filePath, new Set(deps));
      } catch (error) {
        console.error(`Error processing file ${filePath}:`, error);
        dependencies.set(filePath, new Set());
      }
    }
  } catch (error) {
    console.error(`Error scanning directory ${directoryPath}:`, error);
    throw new Error(`Failed to scan directory: ${error.message}`);
  }

  return dependencies;
}