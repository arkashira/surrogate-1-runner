import { Position, Range, TextDocument } from 'vscode';
import { LanguageDetector } from './LanguageDetector';

interface ContextWindow {
  start: number;
  end: number;
  language: string;
}

class ContextExtractor {
  private languageDetector: LanguageDetector;

  constructor(languageDetector: LanguageDetector) {
    this.languageDetector = languageDetector;
  }

  extractContext(document: TextDocument, position: Position): ContextWindow {
    const language = this.languageDetector.detectLanguage(document);
    const contextWindow = this.selectContextWindow(document, position);
    return { ...contextWindow, language };
  }

  private selectContextWindow(document: TextDocument, position: Position): { start: number; end: number } {
    const offset = document.offsetAt(position);
    const start = Math.max(0, offset - 50);
    const end = Math.min(document.getText().length, offset + 50);
    return { start, end };
  }
}

export { ContextExtractor };