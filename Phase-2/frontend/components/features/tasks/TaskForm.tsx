/**
 * Task form component for creating/editing tasks
 * T105: Added due date picker
 * T106: Added recurrence dropdown
 * T115: Responsive layout with 2-column grid on larger screens
 */
"use client"

import { Button } from "@/components/ui/Button"
import { CategoryInput } from "@/components/ui/CategoryInput"
import { DatePicker } from "@/components/ui/DatePicker"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import type { Task, TaskCreate } from "@/types/task"
import { Priority, Recurrence } from "@/types/task"
import { useState } from "react"

export interface TaskFormProps {
  initialData?: Task
  onSubmit: (data: TaskCreate) => void
  onCancel: () => void
  isLoading?: boolean
  existingCategories?: string[]
}

export function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  isLoading,
  existingCategories = [],
}: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreate>({
    title: initialData?.title || "",
    description: initialData?.description || "",
    priority: initialData?.priority || Priority.MEDIUM,
    category: initialData?.category || "",
    due_date: initialData?.due_date || null,
    recurrence: initialData?.recurrence || Recurrence.NONE,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Validate title
    if (!formData.title.trim()) {
      return
    }

    if (formData.title.length > 200) {
      return
    }

    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5">
      <Input
        label="Title"
        type="text"
        value={formData.title}
        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        required
        disabled={isLoading}
        placeholder="Enter task title"
      />

      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Description
        </label>
        <textarea
          id="description"
          value={formData.description || ""}
          onChange={(e) =>
            setFormData({ ...formData, description: e.target.value })
          }
          disabled={isLoading}
          placeholder="Enter task description (optional)"
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Select
          label="Priority"
          value={formData.priority}
          onChange={(e) =>
            setFormData({ ...formData, priority: e.target.value as Priority })
          }
          disabled={isLoading}
          options={[
            { value: Priority.LOW, label: "Low" },
            { value: Priority.MEDIUM, label: "Medium" },
            { value: Priority.HIGH, label: "High" },
          ]}
        />

        <CategoryInput
          label="Category"
          value={formData.category || ""}
          onChange={(value) => setFormData({ ...formData, category: value })}
          suggestions={existingCategories}
          disabled={isLoading}
          placeholder="e.g., Work, Personal, Shopping (optional)"
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <DatePicker
          label="Due Date"
          value={formData.due_date}
          onChange={(value) => setFormData({ ...formData, due_date: value || null })}
          disabled={isLoading}
          placeholder="Select due date (optional)"
        />

        <Select
          label="Recurrence"
          value={formData.recurrence || Recurrence.NONE}
          onChange={(e) =>
            setFormData({ ...formData, recurrence: e.target.value as Recurrence })
          }
          disabled={isLoading}
          options={[
            { value: Recurrence.NONE, label: "None" },
            { value: Recurrence.DAILY, label: "Daily" },
            { value: Recurrence.WEEKLY, label: "Weekly" },
            { value: Recurrence.MONTHLY, label: "Monthly" },
          ]}
        />
      </div>

      <div className="flex gap-3 pt-4">
        <Button type="submit" className="flex-1" disabled={isLoading}>
          {isLoading ? "Saving..." : initialData ? "Update Task" : "Create Task"}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>
      </div>
    </form>
  )
}
