const fs = require('fs');
const path = require('path');
const AstParser = require('./ast-parser');

class Scanner {
  constructor() {
    this.astParser = new AstParser();
  }

  scanDirectory(directoryPath) {
    const files = fs.readdirSync(directoryPath);
    files.forEach((file) => {
      const filePath = path.join(directoryPath, file);
      const stat = fs.statSync(filePath);
      if (stat.isDirectory()) {
        this.scanDirectory(filePath);
      } else if (path.extname(filePath) === '.js' || path.extname(filePath) === '.ts') {
        this.astParser.parseFile(filePath);
      }
    });
  }

  getImports() {
    return this.astParser.getImports();
  }
}

module.exports = Scanner;