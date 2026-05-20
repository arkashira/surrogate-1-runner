import { describe, it, expect } from 'vitest';
import { parseImports } from '../src/parser.js';

describe('parseImports', () => {
  it('should correctly parse static imports', () => {
    const code = `
      import React from 'react';
      import { useState, useEffect } from 'react';
      import axios from 'axios';
    `;

    const imports = parseImports(code);
    expect(imports).toEqual([
      {
        source: 'react',
        specifiers: [{ type: 'ImportDefaultSpecifier', imported: 'React', local: 'React' }]
      },
      {
        source: 'react',
        specifiers: [
          { type: 'ImportSpecifier', imported: 'useState', local: 'useState' },
          { type: 'ImportSpecifier', imported: 'useEffect', local: 'useEffect' }
        ]
      },
      {
        source: 'axios',
        specifiers: [{ type: 'ImportDefaultSpecifier', imported: 'axios', local: 'axios' }]
      }
    ]);
  });

  it('should correctly parse dynamic imports', () => {
    const code = `
      const module = await import('dynamic-module');
    `;

    const imports = parseImports(code);
    expect(imports).toEqual([
      {
        source: 'dynamic-module',
        specifiers: []
      }
    ]);
  });

  it('should handle parsing errors gracefully', () => {
    const invalidCode = 'invalid syntax';
    expect(() => parseImports(invalidCode)).toThrow();
  });
});