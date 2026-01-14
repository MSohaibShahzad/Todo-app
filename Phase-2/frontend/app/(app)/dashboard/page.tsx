/**
 * Dashboard page with task management
 * T110: Added TaskSummary component above task list
 * T111: Added startup notifications showing overdue and due-today counts
 * T129-T133: Added search, filter, and sort functionality
 */
"use client"

import { Button } from "@/components/ui/Button"
import { SearchInput } from "@/components/ui/SearchInput"
import { TaskSummary } from "@/components/features/dashboard/TaskSummary"
import { CreateTaskModal } from "@/components/features/tasks/CreateTaskModal"
import { EditTaskModal } from "@/components/features/tasks/EditTaskModal"
import { FilterControls, FilterState } from "@/components/features/tasks/FilterControls"
import { SortControls, SortOption } from "@/components/features/tasks/SortControls"
import { TaskList } from "@/components/features/tasks/TaskList"
import { deleteTask, toggleTaskComplete } from "@/lib/api/tasks"
import { useTasks } from "@/lib/hooks/useTasks"
import { useToast } from "@/lib/hooks/useToast"
import {
  filterTasks,
  getUniqueCategories,
  searchTasks,
  sortTasks,
} from "@/lib/utils/task-filters"
import type { Task } from "@/types/task"
import { AlertCircle, Calendar, Plus, X } from "lucide-react"
import { useEffect, useMemo, useState } from "react"

export default function DashboardPage() {
  const { tasks, isLoading, mutate } = useTasks()
  const { showSuccess, showError } = useToast()
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [deleteConfirmId, setDeleteConfirmId] = useState<number | null>(null)
  const [showNotifications, setShowNotifications] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [filters, setFilters] = useState<FilterState>({
    priority: "all",
    category: "all",
    status: "all",
  })
  const [sortBy, setSortBy] = useState<SortOption>("created_desc")

  // T129-T133: Apply search, filter, and sort to tasks
  const processedTasks = useMemo(() => {
    let result = [...tasks]
    result = searchTasks(result, searchQuery)
    result = filterTasks(result, filters)
    result = sortTasks(result, sortBy)
    return result
  }, [tasks, searchQuery, filters, sortBy])

  const categories = useMemo(() => getUniqueCategories(tasks), [tasks])

  // T111: Calculate overdue and due today counts for startup notifications
  useEffect(() => {
    if (!isLoading && tasks.length > 0) {
      const hasAlerts =
        tasks.some((t) => t.is_overdue && !t.completed) ||
        tasks.some((t) => t.is_due_today && !t.completed)
      setShowNotifications(hasAlerts)
    }
  }, [tasks, isLoading])

  const overdueCount = tasks.filter((t) => t.is_overdue && !t.completed).length
  const dueTodayCount = tasks.filter((t) => t.is_due_today && !t.completed).length

  const handleComplete = async (id: number, completed: boolean) => {
    try {
      await toggleTaskComplete(id, completed)
      mutate()
      showSuccess(completed ? "Task marked as complete" : "Task marked as incomplete")
    } catch (error) {
      console.error("Failed to toggle task:", error)
      showError("Failed to update task. Please try again.")
    }
  }

  const handleEdit = (task: Task) => {
    setEditingTask(task)
    setIsEditModalOpen(true)
  }

  const handleDelete = (id: number) => {
    setDeleteConfirmId(id)
  }

  const confirmDelete = async () => {
    if (!deleteConfirmId) return

    try {
      await deleteTask(deleteConfirmId)
      mutate()
      setDeleteConfirmId(null)
      showSuccess("Task deleted successfully")
    } catch (error) {
      console.error("Failed to delete task:", error)
      showError("Failed to delete task. Please try again.")
    }
  }

  const completedCount = tasks.filter((t) => t.completed).length
  const totalCount = tasks.length

  return (
    <div>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">My Tasks</h2>
          <p className="text-gray-600 mt-1">
            {processedTasks.length} of {totalCount} tasks · {completedCount} completed
          </p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          New Task
        </Button>
      </div>

      {/* T111: Startup Notifications */}
      {showNotifications && (
        <div className="mb-6 space-y-2">
          {overdueCount > 0 && (
            <div className="flex items-center gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
              <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
              <p className="text-sm text-red-800 flex-1">
                You have {overdueCount} overdue task{overdueCount !== 1 ? "s" : ""}
              </p>
              <button
                onClick={() => setShowNotifications(false)}
                className="text-red-600 hover:text-red-800"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          )}
          {dueTodayCount > 0 && (
            <div className="flex items-center gap-3 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <Calendar className="h-5 w-5 text-yellow-600 flex-shrink-0" />
              <p className="text-sm text-yellow-800 flex-1">
                You have {dueTodayCount} task{dueTodayCount !== 1 ? "s" : ""} due
                today
              </p>
              <button
                onClick={() => setShowNotifications(false)}
                className="text-yellow-600 hover:text-yellow-800"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          )}
        </div>
      )}

      {/* T110: Task Summary Stats */}
      <TaskSummary tasks={tasks} />

      {/* T129: Search Bar */}
      <div className="mb-6">
        <SearchInput
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search by title, description, or category..."
        />
      </div>

      {/* T130-T131: Filter and Sort Controls */}
      <div className="mb-6 space-y-4">
        <FilterControls
          filters={filters}
          onChange={setFilters}
          categories={categories}
        />
        <SortControls sortBy={sortBy} onChange={setSortBy} />
      </div>

      {/* Task List */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading tasks...</p>
        </div>
      ) : processedTasks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">
            {searchQuery || filters.priority !== "all" || filters.category !== "all" || filters.status !== "all"
              ? "No tasks match your filters. Try adjusting your search or filters."
              : "No tasks yet. Create your first task!"}
          </p>
        </div>
      ) : (
        <TaskList
          tasks={processedTasks}
          onComplete={handleComplete}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}

      {/* Create Task Modal */}
      <CreateTaskModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={() => mutate()}
        existingCategories={categories}
      />

      {/* Edit Task Modal */}
      <EditTaskModal
        isOpen={isEditModalOpen}
        task={editingTask}
        onClose={() => {
          setIsEditModalOpen(false)
          setEditingTask(null)
        }}
        onSuccess={() => mutate()}
        existingCategories={categories}
      />

      {/* Delete Confirmation Dialog */}
      {deleteConfirmId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="fixed inset-0 bg-black/50"
            onClick={() => setDeleteConfirmId(null)}
          />
          <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
            <h3 className="text-lg font-semibold mb-2">Delete Task</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete this task? This action cannot be
              undone.
            </p>
            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={() => setDeleteConfirmId(null)}
                className="flex-1"
              >
                Cancel
              </Button>
              <Button
                onClick={confirmDelete}
                className="flex-1 bg-red-600 hover:bg-red-700"
              >
                Delete
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
