import * as acorn from 'acorn';
import * as walk from 'acorn-walk';

/**
 * Parses import statements from JavaScript/TypeScript code.
 * @param {string} code - The source code to parse
 * @returns {Array<{source: string, specifiers: Array<{type: string, imported: string, local: string}>}>}
 * An array of import declarations with their details
 */
export function parseImports(code) {
  try {
    const ast = acorn.parse(code, {
      ecmaVersion: 'latest',
      sourceType: 'module',
      allowHashBang: true
    });

    const imports = [];
    walk.simple(ast, {
      ImportDeclaration(node) {
        imports.push({
          source: node.source.value,
          specifiers: node.specifiers.map(specifier => ({
            type: specifier.type,
            imported: specifier.imported?.name || specifier.local.name,
            local: specifier.local.name
          }))
        });
      },
      CallExpression(node) {
        // Handle dynamic imports
        if (node.callee.type === 'Import' &&
            node.arguments.length > 0 &&
            node.arguments[0].type === 'Literal') {
          imports.push({
            source: node.arguments[0].value,
            specifiers: []
          });
        }
      }
    });

    return imports;
  } catch (error) {
    console.error('Error parsing JavaScript code:', error);
    throw new Error(`Failed to parse JavaScript code: ${error.message}`);
  }
}