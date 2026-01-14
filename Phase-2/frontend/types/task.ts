/**
 * Task type definitions
 */

export enum Priority {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
}

export enum Recurrence {
  NONE = "none",
  DAILY = "daily",
  WEEKLY = "weekly",
  MONTHLY = "monthly",
}

export interface Task {
  id: number
  user_id: number
  title: string
  description: string | null
  completed: boolean
  priority: Priority
  category: string | null
  due_date: string | null
  recurrence: Recurrence
  created_at: string
  updated_at: string
  is_overdue: boolean
  is_due_today: boolean
}

export interface TaskCreate {
  title: string
  description?: string | null
  priority?: Priority
  category?: string | null
  due_date?: string | null
  recurrence?: Recurrence
}

export interface TaskUpdate {
  title?: string
  description?: string | null
  completed?: boolean
  priority?: Priority
  category?: string | null
  due_date?: string | null
  recurrence?: Recurrence
}
