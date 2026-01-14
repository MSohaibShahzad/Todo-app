/**
 * T126-T128: Task filtering and sorting utilities
 */
import type { Task } from "@/types/task"
import type { Priority } from "@/types/task"
import type { SortOption } from "@/components/features/tasks/SortControls"
import type { FilterState } from "@/components/features/tasks/FilterControls"

const priorityOrder: Record<Priority, number> = {
  high: 3,
  medium: 2,
  low: 1,
}

export function filterTasks(tasks: Task[], filters: FilterState): Task[] {
  return tasks.filter((task) => {
    // Filter by priority
    if (filters.priority !== "all" && task.priority !== filters.priority) {
      return false
    }

    // Filter by category
    if (filters.category !== "all" && task.category !== filters.category) {
      return false
    }

    // Filter by status
    if (filters.status === "pending" && task.completed) {
      return false
    }
    if (filters.status === "completed" && !task.completed) {
      return false
    }

    return true
  })
}

export function sortTasks(tasks: Task[], sortBy: SortOption): Task[] {
  const sorted = [...tasks]

  switch (sortBy) {
    case "created_asc":
      return sorted.sort(
        (a, b) =>
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      )
    case "created_desc":
      return sorted.sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      )
    case "due_date_asc":
      return sorted.sort((a, b) => {
        if (!a.due_date) return 1
        if (!b.due_date) return -1
        return new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
      })
    case "due_date_desc":
      return sorted.sort((a, b) => {
        if (!a.due_date) return 1
        if (!b.due_date) return -1
        return new Date(b.due_date).getTime() - new Date(a.due_date).getTime()
      })
    case "priority_desc":
      return sorted.sort(
        (a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]
      )
    case "priority_asc":
      return sorted.sort(
        (a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]
      )
    case "title_asc":
      return sorted.sort((a, b) => a.title.localeCompare(b.title))
    case "title_desc":
      return sorted.sort((a, b) => b.title.localeCompare(a.title))
    default:
      return sorted
  }
}

export function searchTasks(tasks: Task[], query: string): Task[] {
  if (!query.trim()) return tasks

  const lowerQuery = query.toLowerCase()
  return tasks.filter(
    (task) =>
      task.title.toLowerCase().includes(lowerQuery) ||
      task.description?.toLowerCase().includes(lowerQuery) ||
      task.category?.toLowerCase().includes(lowerQuery)
  )
}

export function getUniqueCategories(tasks: Task[]): string[] {
  const categories = tasks
    .map((task) => task.category)
    .filter((cat): cat is string => !!cat)
  return Array.from(new Set(categories)).sort()
}
