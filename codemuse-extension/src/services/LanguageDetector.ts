import { TextDocument } from 'vscode';

interface Language {
  name: string;
  extensions: string[];
}

class LanguageDetector {
  private languages: Language[];

  constructor(languages: Language[]) {
    this.languages = languages;
  }

  detectLanguage(document: TextDocument): string {
    const fileExtension = document.fileName.split('.').pop();
    for (const language of this.languages) {
      if (language.extensions.includes(fileExtension)) {
        return language.name;
      }
    }
    return 'unknown';
  }
}

export { LanguageDetector };