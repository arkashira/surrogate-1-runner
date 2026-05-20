export interface Summary {
  id: string;
  title: string;
  content: string;
  tags: string[];
  created_at: string;   // ISO‑like string, e.g. "2024-05-20 14:30"
  model: string;
  source: string;
}

/**
 * The shape of the callback that receives the *current* list of selected tags.
 * It is called **after** the internal state has been updated.
 */
export type TagFilterChangeHandler = (selectedTags: string[]) => void;