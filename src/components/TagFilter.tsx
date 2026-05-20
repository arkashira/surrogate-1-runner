import React from "react";

interface TagFilterProps {
  /** All possible tags that can be selected */
  availableTags: string[];
  /** Currently selected tags */
  selectedTags: string[];
  /** Called when a checkbox is toggled */
  onToggle: (tag: string, checked: boolean) => void;
}

/**
 * Simple list of checkboxes. No styling assumptions – the parent can wrap it
 * in any container (card, modal, sidebar, …).
 */
export const TagFilter: React.FC<TagFilterProps> = ({
  availableTags,
  selectedTags,
  onToggle,
}) => {
  return (
    <div className="flex flex-wrap gap-2">
      {availableTags.map((tag) => (
        <label key={tag} className="flex items-center space-x-2">
          <input
            type="checkbox"
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            checked={selectedTags.includes(tag)}
            onChange={(e) => onToggle(tag, e.target.checked)}
          />
          <span className="text-sm text-gray-700">{tag}</span>
        </label>
      ))}
    </div>
  );
};