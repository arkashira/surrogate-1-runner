import { Document } from '../types';

type FilterState = {
  query: string;
  fileType: string | null;   // e.g. 'pdf', 'epub', 'docx', 'book'
  dateAdded: Date | null;    // inclusive lower bound
};

type Listener = () => void;

const STORAGE_KEY = 'libraryFilterState';

function loadState(): FilterState {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return { query: '', fileType: null, dateAdded: null };
    const parsed = JSON.parse(raw);
    return {
      query: parsed.query || '',
      fileType: parsed.fileType || null,
      dateAdded: parsed.dateAdded ? new Date(parsed.dateAdded) : null,
    };
  } catch {
    return { query: '', fileType: null, dateAdded: null };
  }
}

let state: FilterState = loadState();
let listeners: Listener[] = [];
let documents: Document[] = [];

function saveState() {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
      query: state.query,
      fileType: state.fileType,
      dateAdded: state.dateAdded ? state.dateAdded.toISOString() : null,
    }));
  } catch {
    // ignore storage failures in restricted environments
  }
}

function emit() {
  listeners.forEach((l) => l());
}

function scoreDocument(doc: Document, query: string): number {
  if (!query) return 1;
  const q = query.toLowerCase().trim();
  const title = doc.title.toLowerCase();
  const author = (doc.author || '').toLowerCase();
  const body = (doc.content || '').toLowerCase();

  if (title.includes(q)) return 2;
  if (author.includes(q)) return 1.8;
  if (body.includes(q)) return 1;
  return 0;
}

function matchesFilters(doc: Document): boolean {
  if (state.fileType && doc.fileType !== state.fileType) return false;
  if (state.dateAdded) {
    const added = new Date(doc.dateAdded);
    if (isNaN(added.getTime()) || added < state.dateAdded) return false;
  }
  return true;
}

export function setDocuments(docs: Document[]) {
  documents = docs;
  emit();
}

export function setQuery(query: string) {
  state.query = query;
  saveState();
  emit();
}

export function setFileType(fileType: string | null) {
  state.fileType = fileType;
  saveState();
  emit();
}

export function setDateAdded(dateAdded: Date | null) {
  state.dateAdded = dateAdded;
  saveState();
  emit();
}

export function resetFilters() {
  state = { query: '', fileType: null, dateAdded: null };
  saveState();
  emit();
}

export function subscribe(listener: Listener) {
  listeners.push(listener);
  return () => {
    listeners = listeners.filter((l) => l !== listener);
  };
}

export function getResults(): Document[] {
  const q = state.query.toLowerCase().trim();
  const filtered = documents.filter(matchesFilters);

  if (!q) return filtered;

  return filtered
    .map((doc) => ({ doc, score: scoreDocument(doc, state.query) }))
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score)
    .map(({ doc }) => doc);
}

export function getStateSnapshot() {
  return { ...state };
}