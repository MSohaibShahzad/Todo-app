/**
 * T125: SortControls component for sorting tasks
 */
"use client"

import { Select } from "@/components/ui/Select"

export type SortOption =
  | "created_asc"
  | "created_desc"
  | "due_date_asc"
  | "due_date_desc"
  | "priority_asc"
  | "priority_desc"
  | "title_asc"
  | "title_desc"

export interface SortControlsProps {
  sortBy: SortOption
  onChange: (sortBy: SortOption) => void
}

export function SortControls({ sortBy, onChange }: SortControlsProps) {
  return (
    <div className="w-full sm:w-64">
      <Select
        label="Sort by"
        value={sortBy}
        onChange={(e) => onChange(e.target.value as SortOption)}
        options={[
          { value: "created_desc", label: "Newest First" },
          { value: "created_asc", label: "Oldest First" },
          { value: "due_date_asc", label: "Due Date (Earliest)" },
          { value: "due_date_desc", label: "Due Date (Latest)" },
          { value: "priority_desc", label: "Priority (High to Low)" },
          { value: "priority_asc", label: "Priority (Low to High)" },
          { value: "title_asc", label: "Title (A to Z)" },
          { value: "title_desc", label: "Title (Z to A)" },
        ]}
      />
    </div>
  )
}
