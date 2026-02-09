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
    <form onSubmit={handleSubmit} className="space-y-5 sm:space-y-6">
      {/* Title Input */}
      <div className="space-y-2">
        <label htmlFor="title" className="block text-sm font-semibold text-white/90">
          Title <span className="text-red-400">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
          disabled={isLoading}
          placeholder="Enter task title"
          className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-[#3B82F6]/50 backdrop-blur-sm transition-all disabled:opacity-50"
        />
      </div>

      {/* Description Textarea */}
      <div className="space-y-2">
        <label
          htmlFor="description"
          className="block text-sm font-semibold text-white/90"
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
          rows={4}
          className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-[#3B82F6]/50 backdrop-blur-sm transition-all resize-none disabled:opacity-50"
        />
      </div>

      {/* Priority and Category Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label htmlFor="priority" className="block text-sm font-semibold text-white/90">
            Priority
          </label>
          <select
            id="priority"
            value={formData.priority}
            onChange={(e) =>
              setFormData({ ...formData, priority: e.target.value as Priority })
            }
            disabled={isLoading}
            className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-[#3B82F6]/50 backdrop-blur-sm transition-all disabled:opacity-50 appearance-none cursor-pointer"
          >
            <option value={Priority.LOW} className="bg-[#1A1F2E] text-white">Low Priority</option>
            <option value={Priority.MEDIUM} className="bg-[#1A1F2E] text-white">Medium Priority</option>
            <option value={Priority.HIGH} className="bg-[#1A1F2E] text-white">High Priority</option>
          </select>
        </div>

        <CategoryInput
          label="Category"
          value={formData.category || ""}
          onChange={(value) => setFormData({ ...formData, category: value })}
          suggestions={existingCategories}
          disabled={isLoading}
          placeholder="e.g., Work, Personal"
        />
      </div>

      {/* Due Date and Recurrence Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <DatePicker
          label="Due Date"
          value={formData.due_date ?? null}
          onChange={(value) => setFormData({ ...formData, due_date: value || null })}
          disabled={isLoading}
          placeholder="Select due date"
        />

        <div className="space-y-2">
          <label htmlFor="recurrence" className="block text-sm font-semibold text-white/90">
            Recurrence
          </label>
          <select
            id="recurrence"
            value={formData.recurrence || Recurrence.NONE}
            onChange={(e) =>
              setFormData({ ...formData, recurrence: e.target.value as Recurrence })
            }
            disabled={isLoading}
            className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-[#3B82F6]/50 backdrop-blur-sm transition-all disabled:opacity-50 appearance-none cursor-pointer"
          >
            <option value={Recurrence.NONE} className="bg-[#1A1F2E] text-white">No Recurrence</option>
            <option value={Recurrence.DAILY} className="bg-[#1A1F2E] text-white">Daily</option>
            <option value={Recurrence.WEEKLY} className="bg-[#1A1F2E] text-white">Weekly</option>
            <option value={Recurrence.MONTHLY} className="bg-[#1A1F2E] text-white">Monthly</option>
          </select>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 pt-6 border-t border-white/10">
        <Button
          type="submit"
          className="flex-1 bg-gradient-to-r from-[#3B82F6] to-[#06B6D4] hover:shadow-lg hover:shadow-[#3B82F6]/50 transition-all"
          disabled={isLoading}
        >
          {isLoading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Saving...
            </span>
          ) : (
            initialData ? "Update Task" : "Create Task"
          )}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isLoading}
          className="bg-white/5 border-white/20 text-white hover:bg-white/10 hover:border-white/30"
        >
          Cancel
        </Button>
      </div>
    </form>
  )
}
