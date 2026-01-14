/**
 * T122-T124: FilterControls component for filtering tasks by priority, category, and status
 */
"use client"

import { Select } from "@/components/ui/Select"
import { Priority } from "@/types/task"

export interface FilterState {
  priority: string
  category: string
  status: string
}

export interface FilterControlsProps {
  filters: FilterState
  onChange: (filters: FilterState) => void
  categories: string[]
}

export function FilterControls({
  filters,
  onChange,
  categories,
}: FilterControlsProps) {
  const handleFilterChange = (key: keyof FilterState, value: string) => {
    onChange({ ...filters, [key]: value })
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <Select
        label="Priority"
        value={filters.priority}
        onChange={(e) => handleFilterChange("priority", e.target.value)}
        options={[
          { value: "all", label: "All Priorities" },
          { value: Priority.HIGH, label: "High" },
          { value: Priority.MEDIUM, label: "Medium" },
          { value: Priority.LOW, label: "Low" },
        ]}
      />

      <Select
        label="Category"
        value={filters.category}
        onChange={(e) => handleFilterChange("category", e.target.value)}
        options={[
          { value: "all", label: "All Categories" },
          ...categories.map((cat) => ({ value: cat, label: cat })),
        ]}
      />

      <Select
        label="Status"
        value={filters.status}
        onChange={(e) => handleFilterChange("status", e.target.value)}
        options={[
          { value: "all", label: "All Tasks" },
          { value: "pending", label: "Pending" },
          { value: "completed", label: "Completed" },
        ]}
      />
    </div>
  )
}
