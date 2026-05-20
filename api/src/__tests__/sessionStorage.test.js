/**
 * @jest-environment jsdom
 */

import {
  set,
  get,
  remove,
  clear,
} from '../sessionStorage';

describe('sessionStorage wrapper', () => {
  beforeEach(() => {
    clear();
  });

  test('set and get primitive values', () => {
    set('foo', 42);
    expect(get('foo')).toBe(42);
  });

  test('set and get object values', () => {
    const obj = { a: 1, b: 'text' };
    set('obj', obj);
    expect(get('obj')).toEqual(obj);
  });

  test('get returns default when key missing', () => {
    expect(get('missing', 'default')).toBe('default');
  });

  test('remove deletes key', () => {
    set('temp', 'value');
    remove('temp');
    expect(get('temp')).toBeNull();
  });

  test('clear removes all keys', () => {
    set('one', 1);
    set('two', 2);
    clear();
    expect(get('one')).toBeNull();
    expect(get('two')).toBeNull();
  });

  test('handles JSON parse errors gracefully', () => {
    // Directly manipulate the underlying storage to inject bad JSON
    const key = 'bad';
    window.localStorage.setItem('axentx:' + key, '{invalid json}');
    expect(get(key, 'fallback')).toBe('fallback');
  });
});