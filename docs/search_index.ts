import { searchConfig } from './search_config';

interface DocEntry {
  path: string;
  category: string;
  content: string;
  searchable: boolean;
  weight: number;
  aliases?: string[];
  prominent?: boolean;
}

class SearchIndex {
  private index: Map<string, DocEntry>;

  constructor() {
    this.index = new Map<string, DocEntry>();
  }

  async loadIndex() {
    const config = searchConfig;
    const migrationGuidePath = '/docs/migration-guide.md';
    const migrationGuideContent = await readDoc(migrationGuidePath);

    // Index migration guide with high priority
    this.index.set('migration', {
      path: migrationGuidePath,
      category: 'Getting Started',
      content: migrationGuideContent,
      searchable: true,
      weight: 1.0,
      aliases: ['migration', 'upgrade', 'guide'],
      prominent: true
    });

    // Index all Getting Started docs
    const gettingStartedDir = '/docs/getting-started/';
    const files = await listDir(gettingStartedDir);

    for (const file of files) {
      const fullPath = `${gettingStartedDir}${file}`;
      const content = await readDoc(fullPath);

      this.index.set(file, {
        path: fullPath,
        category: 'Getting Started',
        content,
        searchable: true,
        weight: 0.8
      });
    }
  }

  async search(query: string): Promise<DocEntry[]> {
    const results: DocEntry[] = [];

    for (const [key, entry] of this.index.entries()) {
      if (entry.searchable && matchesQuery(query, entry)) {
        results.push(entry);
      }
    }

    return results.sort((a, b) => {
      // Prioritize Getting Started category
      if (a.category === 'Getting Started' && b.category !== 'Getting Started') return -1;
      if (a.category !== 'Getting Started' && b.category === 'Getting Started') return 1;

      // Prioritize migration guide
      if (a.path.includes('migration-guide') && !b.path.includes('migration-guide')) return -1;
      if (!a.path.includes('migration-guide') && b.path.includes('migration-guide')) return 1;

      return 0;
    });
  }

  async matchesQuery(query: string, entry: DocEntry): Promise<boolean> {
    const searchTerms = query.toLowerCase().split(/\s+/);

    for (const term of searchTerms) {
      if (entry.content.toLowerCase().includes(term) ||
          entry.aliases?.includes(term.toLowerCase())) {
        return true;
      }
    }

    return false;
  }

  async readDoc(path: string): Promise<string> {
    // Implementation would read actual file content
    return '';
  }

  async listDir(path: string): Promise<string[]> {
    // Implementation would list directory contents
    return [];
  }
}

const searchIndex = new SearchIndex();
searchIndex.loadIndex();

export async function searchDocs(query: string): Promise<DocEntry[]> {
  return searchIndex.search(query);
}