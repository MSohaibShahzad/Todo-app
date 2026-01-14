/**
 * Task list component rendering array of tasks
 * T113: Responsive grid layout (1 col mobile, 2 col tablet, 3 col desktop)
 */
"use client"

import type { Task } from "@/types/task"
import { TaskCard } from "./TaskCard"

export interface TaskListProps {
  tasks: Task[]
  onComplete: (id: number, completed: boolean) => void
  onEdit: (task: Task) => void
  onDelete: (id: number) => void
}

export function TaskList({ tasks, onComplete, onEdit, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No tasks yet. Create your first task!</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onComplete={onComplete}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
