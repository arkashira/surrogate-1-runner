import { useState, useMemo, useCallback } from "react";
import { Summary, TagFilterChangeHandler } from "../types";

/**
 * Hook that:
 *   1️⃣ Holds the list of selected tags.
 *   2️⃣ Provides a memoised list of summaries filtered by those tags.
 *   3️⃣ Exposes a stable `toggleTag` function for UI controls.
 *
 * The filter mode can be "OR" (default – a summary appears if **any** selected tag matches)
 * or "AND" (summary must contain **all** selected tags). The mode is configurable via the
 * `filterMode` argument.
 */
export function useTagFilter(
  summaries: Summary[],
  onChange?: TagFilterChangeHandler,
  filterMode: "OR" | "AND" = "OR"
) {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  // -------------------------------------------------------------------------
  // 1️⃣ Toggle a tag (checkbox click)
  // -------------------------------------------------------------------------
  const toggleTag = useCallback(
    (tag: string, checked: boolean) => {
      setSelectedTags((prev) => {
        const next = checked ? [...prev, tag] : prev.filter((t) => t !== tag);
        // Notify parent *after* state is resolved
        onChange?.(next);
        return next;
      });
    },
    [onChange]
  );

  // -------------------------------------------------------------------------
  // 2️⃣ Compute filtered summaries – memoised for performance
  // -------------------------------------------------------------------------
  const filteredSummaries = useMemo(() => {
    if (selectedTags.length === 0) return summaries;

    return summaries.filter((summary) => {
      const hasTag = summary.tags ?? [];

      if (filterMode === "OR") {
        // At least one selected tag present
        return selectedTags.some((t) => hasTag.includes(t));
      } else {
        // ALL selected tags must be present
        return selectedTags.every((t) => hasTag.includes(t));
      }
    });
  }, [summaries, selectedTags, filterMode]);

  return { selectedTags, toggleTag, filteredSummaries };
}