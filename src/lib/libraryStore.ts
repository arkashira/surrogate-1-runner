import { create } from 'zustand';
import { persist } from 'zustand/middleware';

+ const MAX_RECENT = 50; // reasonable session cap

export interface LibraryDocument {
  id: string;
  name: string;
  path: string;
  mimeType: string;
  size: number;
  createdAt: string;
  updatedAt: string;
+ lastOpenedAt?: number;
}

interface LibraryState {
  documents: LibraryDocument[];
  selectedId: string | null;
+ recentlyOpenedIds: string[];
  loading: boolean;
  error: string | null;

  setDocuments: (documents: LibraryDocument[]) => void;
  selectDocument: (id: string | null) => void;
+ openDocument: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
+ getOrderedDocuments: () => LibraryDocument[];
}

export const useLibraryStore = create<LibraryState>()(
  persist(
    (set, get) => ({
      documents: [],
      selectedId: null,
+     recentlyOpenedIds: [],
      loading: false,
      error: null,

      setDocuments: (documents) => set({ documents }),
      selectDocument: (id) => set({ selectedId: id }),
+     openDocument: (id) => {
+       const state = get();
+       const doc = state.documents.find((d) => d.id === id);
+       if (!doc) return;
+
+       // Update last opened timestamp
+       const updatedDocuments = state.documents.map((d) =>
+         d.id === id ? { ...d, lastOpenedAt: Date.now() } : d
+       );
+
+       // Update recently opened list (move to front, dedupe, cap)
+       let recent = [id, ...state.recentlyOpenedIds.filter((rid) => rid !== id)];
+       if (recent.length > MAX_RECENT) recent = recent.slice(0, MAX_RECENT);
+
+       // Track active event for MAU (lightweight, non-blocking)
+       if (typeof window !== 'undefined' && (window as any).axentxTrack) {
+         try {
+           (window as any).axentxTrack('active', { documentId: id, name: doc.name });
+         } catch (e) {
+           // best-effort tracking
+         }
+       }
+
+       set({
+         documents: updatedDocuments,
+         recentlyOpenedIds: recent,
+         selectedId: id,
+       });
+     },
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),
+     getOrderedDocuments: () => {
+       const state = get();
+       const { documents, recentlyOpenedIds } = state;
+
+       if (recentlyOpenedIds.length === 0) return documents;
+
+       const recentSet = new Set(recentlyOpenedIds);
+       const recentDocs = recentlyOpenedIds
+         .map((id) => documents.find((d) => d.id === id))
+         .filter(Boolean) as LibraryDocument[];
+       const otherDocs = documents.filter((d) => !recentSet.has(d.id));
+
+       return [...recentDocs, ...otherDocs];
+     },
    }),
    {
      name: 'library-storage',
      partialize: (state) => ({
        // persist only non-session data
        documents: state.documents,
        selectedId: state.selectedId,
        // do NOT persist recentlyOpenedIds across reloads (session-only)
      }),
    }
  )
);