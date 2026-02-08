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
import { motion } from "framer-motion"

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
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A0E1A] via-[#1A1F2E] to-[#232936] -m-6 p-6">
      {/* Animated Background Blobs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute w-96 h-96 rounded-full bg-[#8B5CF6] opacity-20 blur-3xl"
          animate={{
            x: mousePosition.x / 20,
            y: mousePosition.y / 20,
            scale: [1, 1.2, 1],
          }}
          transition={{ duration: 3, repeat: Infinity }}
          style={{ top: "10%", left: "10%" }}
        />
        <motion.div
          className="absolute w-96 h-96 rounded-full bg-[#06B6D4] opacity-30 blur-3xl"
          animate={{
            x: -mousePosition.x / 30,
            y: -mousePosition.y / 30,
            scale: [1, 1.3, 1],
          }}
          transition={{ duration: 4, repeat: Infinity }}
          style={{ bottom: "10%", right: "10%" }}
        />
      </div>

      <div className="relative z-10">
        {/* Header */}
        <motion.div
          className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-white">My Tasks</h2>
            <p className="text-white/70 mt-1">
              {processedTasks.length} of {totalCount} tasks · {completedCount} completed
            </p>
          </div>
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              onClick={() => setIsCreateModalOpen(true)}
              className="bg-gradient-to-r from-[#3B82F6] to-[#06B6D4] hover:shadow-lg hover:shadow-[#3B82F6]/50"
            >
              <Plus className="h-4 w-4 mr-2" />
              New Task
            </Button>
          </motion.div>
        </motion.div>

        {/* T111: Startup Notifications */}
        {showNotifications && (
          <motion.div
            className="mb-6 space-y-2"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            {overdueCount > 0 && (
              <motion.div
                className="flex items-center gap-3 p-4 bg-red-500/20 backdrop-blur-sm border border-red-400/30 rounded-xl"
                whileHover={{ scale: 1.01 }}
              >
                <AlertCircle className="h-5 w-5 text-red-300 flex-shrink-0" />
                <p className="text-sm text-red-100 flex-1">
                  You have {overdueCount} overdue task{overdueCount !== 1 ? "s" : ""}
                </p>
                <button
                  onClick={() => setShowNotifications(false)}
                  className="text-red-300 hover:text-red-100"
                >
                  <X className="h-4 w-4" />
                </button>
              </motion.div>
            )}
            {dueTodayCount > 0 && (
              <motion.div
                className="flex items-center gap-3 p-4 bg-yellow-500/20 backdrop-blur-sm border border-yellow-400/30 rounded-xl"
                whileHover={{ scale: 1.01 }}
              >
                <Calendar className="h-5 w-5 text-yellow-300 flex-shrink-0" />
                <p className="text-sm text-yellow-100 flex-1">
                  You have {dueTodayCount} task{dueTodayCount !== 1 ? "s" : ""} due
                  today
                </p>
                <button
                  onClick={() => setShowNotifications(false)}
                  className="text-yellow-300 hover:text-yellow-100"
                >
                  <X className="h-4 w-4" />
                </button>
              </motion.div>
            )}
          </motion.div>
        )}

        {/* T110: Task Summary Stats */}
        <TaskSummary tasks={tasks} />

        {/* T129: Search Bar */}
        <motion.div
          className="mb-6"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <SearchInput
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search by title, description, or category..."
          />
        </motion.div>

        {/* T130-T131: Filter and Sort Controls */}
        <motion.div
          className="mb-6 space-y-4"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <FilterControls
            filters={filters}
            onChange={setFilters}
            categories={categories}
          />
          <SortControls sortBy={sortBy} onChange={setSortBy} />
        </motion.div>

        {/* Task List */}
        {isLoading ? (
          <motion.div
            className="text-center py-12"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <p className="text-white/70">Loading tasks...</p>
          </motion.div>
        ) : processedTasks.length === 0 ? (
          <motion.div
            className="text-center py-12 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <p className="text-white/70">
              {searchQuery || filters.priority !== "all" || filters.category !== "all" || filters.status !== "all"
                ? "No tasks match your filters. Try adjusting your search or filters."
                : "No tasks yet. Create your first task!"}
            </p>
          </motion.div>
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
            <motion.div
              className="fixed inset-0 bg-black/70 backdrop-blur-sm"
              onClick={() => setDeleteConfirmId(null)}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            />
            <motion.div
              className="relative bg-gradient-to-br from-[#232936] to-[#1A1F2E] rounded-xl shadow-2xl max-w-md w-full mx-4 p-6 border border-white/20"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
            >
              <h3 className="text-lg font-semibold mb-2 text-white">Delete Task</h3>
              <p className="text-white/70 mb-6">
                Are you sure you want to delete this task? This action cannot be
                undone.
              </p>
              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={() => setDeleteConfirmId(null)}
                  className="flex-1 bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20"
                >
                  Cancel
                </Button>
                <Button
                  onClick={confirmDelete}
                  className="flex-1 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 hover:shadow-lg hover:shadow-red-500/50"
                >
                  Delete
                </Button>
              </div>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  )
}
