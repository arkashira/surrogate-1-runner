import { ContextExtractor } from '../ContextExtractor';
import { LanguageDetector } from '../LanguageDetector';
import { TextDocument } from 'vscode';

describe('ContextExtractor', () => {
  it('extracts context window', () => {
    const languageDetector = new LanguageDetector([
      { name: 'javascript', extensions: ['js'] },
    ]);
    const contextExtractor = new ContextExtractor(languageDetector);
    const document = {
      getText: () => 'Hello World',
      offsetAt: (position: any) => 5,
      fileName: 'example.js',
    } as any;
    const position = { line: 0, character: 5 } as any;
    const contextWindow = contextExtractor.extractContext(document, position);
    expect(contextWindow).toEqual({
      start: 0,
      end: 11,
      language: 'javascript',
    });
  });
});