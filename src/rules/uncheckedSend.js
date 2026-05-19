/**
 * Rule: uncheckedSend
 *
 * Detects calls to .send() or .transfer() that are not checked for success.
 * Flags them with severity "Medium" and provides a remediation link.
 *
 * The rule is written as an ESLint-compatible rule module so it can be
 * integrated with the surrogate-1 linter which expects each rule to export
 * an object with `meta` and `create` properties.
 */
"use strict";

module.exports = {
  meta: {
    type: "problem",
    docs: {
      description: "Detects unchecked send/transfer calls",
      category: "Security",
      recommended: true,
      severity: "medium",
    },
    schema: [],
    fixable: null,
    messages: {
      uncheckedSend: "Unchecked {{method}} call. Consider checking the return value or using call{} instead.",
    },
  },

  create(context) {
    const sourceCode = context.getSourceCode();

    /**
     * Check if a CallExpression's result is being checked
     * @param {ASTNode} node - The CallExpression node
     * @returns {boolean} - True if the call is unchecked
     */
    function isUncheckedCall(node) {
      const parent = node.parent;
      
      // Check if result is assigned to a variable
      if (parent.type === 'VariableDeclarator' && parent.init === node) {
        return false; // Assigned to variable - potentially checked
      }
      
      // Check if used in require/assert
      if (parent.type === 'CallExpression' && 
          (parent.callee.name === 'require' || parent.callee.name === 'assert')) {
        return false;
      }
      
      // Check if used in ternary
      if (parent.type === 'ConditionalExpression') {
        return false;
      }
      
      return true; // Unchecked
    }

    return {
      CallExpression(node) {
        // Check for .send() or .transfer() calls
        if (node.callee.type !== 'MemberExpression') return;
        
        const methodName = node.callee.property.name;
        
        if (methodName !== 'send' && methodName !== 'transfer') return;
        
        // Verify it's a Solidity-compatible call (has arguments)
        if (node.arguments.length === 0) return;
        
        // Check if unchecked
        if (isUncheckedCall(node)) {
          context.report({
            node,
            messageId: 'uncheckedSend',
            data: { method: methodName },
          });
        }
      },
    };
  },
};