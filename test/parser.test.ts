import { Parser } from '../src/parser';
import { config } from '../src/config';

describe('Parser', () => {
  it('should use streaming parser by default', () => {
    const parser = new Parser();
    const result = parser.parse('test data');
    expect(result).toEqual({ result: 'streaming', data: 'test data' });
  });

  it('should use legacy parser when flag is false', () => {
    config.get = jest.fn().mockReturnValue(false);
    const parser = new Parser();
    const result = parser.parse('test data');
    expect(result).toEqual({ result: 'legacy', data: 'test data' });
  });

  it('should override flag with environment variable', () => {
    process.env.PARSER_STREAMING_ENABLED = 'false';
    const parser = new Parser();
    const result = parser.parse('test data');
    expect(result).toEqual({ result: 'legacy', data: 'test data' });
  });
});