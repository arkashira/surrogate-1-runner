export interface Document {
  id: string;
  title: string;
  author: string;
  body: string;
  fileType: 'pdf' | 'epub' | 'mobi' | 'txt';
  dateAdded: string; // ISO date
}

export interface Filters {
  fileTypes: string[];
  dateFrom?: string;
  dateTo?: string;
}

export interface RankedDocument extends Document {
  score: number;
}

function tokenize(text: string): Set<string> {
  return new Set(text.toLowerCase().split(/\s+/).filter(Boolean));
}

function scoreMatch(fieldTokens: Set<string>, queryTokens: Set<string>): number {
  let matches = 0;
  for (const qt of queryTokens) {
    if (fieldTokens.has(qt)) matches++;
  }
  return matches;
}

export function rankDocuments(
  query: string,
  documents: Document[],
  filters: Filters
): RankedDocument[] {
  const q = query.trim().toLowerCase();
  const hasQuery = q.length > 0;
  const hasFileFilter = Array.isArray(filters.fileTypes) && filters.fileTypes.length > 0;
  const hasDateFilter = Boolean(filters.dateFrom || filters.dateTo);

  // Short-circuit: no query and no filters -> return all with score 0
  if (!hasQuery && !hasFileFilter && !hasDateFilter) {
    return documents.map((d) => ({ ...d, score: 0 }));
  }

  const queryTokens = hasQuery ? tokenize(q) : null;
  const lowerFileTypes = hasFileFilter
    ? filters.fileTypes.map((t) => t.toLowerCase())
    : null;

  const scored: RankedDocument[] = [];

  for (const doc of documents) {
    // File-type filter
    if (lowerFileTypes && !lowerFileTypes.includes(doc.fileType.toLowerCase())) {
      continue;
    }
    // Date filters
    if (filters.dateFrom && doc.dateAdded < filters.dateFrom) continue;
    if (filters.dateTo && doc.dateAdded > filters.dateTo) continue;

    // If no query, include filtered docs with score 0
    if (!hasQuery) {
      scored.push({ ...doc, score: 0 });
      continue;
    }

    const titleTokens = tokenize(doc.title);
    const authorTokens = tokenize(doc.author);
    const bodyTokens = tokenize(doc.body);

    const exactTitle = doc.title.toLowerCase() === q ? 3 : 0;
    const exactAuthor = doc.author.toLowerCase() === q ? 2 : 0;

    const titleMatches = queryTokens ? scoreMatch(titleTokens, queryTokens) : 0;
    const authorMatches = queryTokens ? scoreMatch(authorTokens, queryTokens) : 0;
    const bodyMatches = queryTokens ? scoreMatch(bodyTokens, queryTokens) : 0;

    // Tiered scoring:
    // exact title (×3) > exact author (×2) > token title/author (×1.5) > body (×1)
    const score =
      exactTitle * 100 +
      exactAuthor * 80 +
      titleMatches * 15 +
      authorMatches * 10 +
      bodyMatches * 5;

    if (score > 0) {
      scored.push({ ...doc, score });
    }
  }

  return scored.sort((a, b) => b.score - a.score);
}