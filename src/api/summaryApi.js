// ---------------------------------------------------------------
// src/api/summaryApi.ts
// ---------------------------------------------------------------
import axios from 'axios';

export interface Summary {
  id: string;
  title: string;
  snippet: string;
  source: string;
  date: string;               // ISO string
  category?: string;
  keywords?: string[];
  author?: string;
  model?: string;
  sourceLanguage?: string;
  sourceFormat?: string;
  sourceDomain?: string;
  sourceURL?: string;
  sourceURLDomain?: string;
  sourceURLPath?: string;
  sourceURLQuery?: string;
}

/**
 * GET /summaries – returns the full catalogue.
 */
export const getSummaries = async (): Promise<Summary[]> => {
  const { data } = await axios.get<Summary[]>('/api/summaries');
  return data;
};

/**
 * GET /summaries/search?q=… – server‑side fuzzy search.
 * The backend can be a simple ElasticSearch proxy or a vector‑store lookup.
 */
export const searchSummaries = async (query: string): Promise<Summary[]> => {
  const { data } = await axios.get<Summary[]>('/api/summaries/search', {
    params: { q: query },
  });
  return data;
};