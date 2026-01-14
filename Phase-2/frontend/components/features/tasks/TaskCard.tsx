/**
 * Task card component displaying individual task
 * T092: Updated to display priority badge with correct color
 * T093: Updated to display category label if present
 * T104: Updated to display due date with OVERDUE/DUE TODAY badges
 * T114: Responsive padding (smaller on mobile, larger on desktop)
 * T119-T120: Touch-friendly icon buttons (40px on mobile, 32px on desktop)
 */
"use client"

import { Badge, PriorityBadge } from "@/components/ui/Badge"
import { Button } from "@/components/ui/Button"
import { Card, CardContent } from "@/components/ui/Card"
import { formatDueDate, isOverdue, isDueToday } from "@/lib/utils/date-formatting"
import type { Task } from "@/types/task"
import { Calendar, Check, Edit, Trash2, X } from "lucide-react"

export interface TaskCardProps {
  task: Task
  onComplete: (id: number, completed: boolean) => void
  onEdit: (task: Task) => void
  onDelete: (id: number) => void
}

export function TaskCard({ task, onComplete, onEdit, onDelete }: TaskCardProps) {
  return (
    <Card className={task.completed ? "opacity-60" : ""}>
      <CardContent className="p-3 sm:p-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2 flex-wrap">
              <h3
                className={`font-medium text-gray-900 ${
                  task.completed ? "line-through" : ""
                }`}
              >
                {task.title}
              </h3>
              <PriorityBadge priority={task.priority} />
              {task.category && (
                <Badge variant="default" size="sm">
                  📁 {task.category}
                </Badge>
              )}
            </div>
            {task.description && (
              <p className="text-sm text-gray-600 mb-2">{task.description}</p>
            )}
            {task.due_date && (
              <div className="flex items-center gap-2 mt-2">
                <Calendar className="h-4 w-4 text-gray-400" />
                <span className="text-sm text-gray-600">
                  {formatDueDate(task.due_date)}
                </span>
                {isOverdue(task.due_date, task.completed) && (
                  <Badge variant="danger" size="sm">
                    OVERDUE
                  </Badge>
                )}
                {isDueToday(task.due_date) && !task.completed && (
                  <Badge variant="warning" size="sm">
                    DUE TODAY
                  </Badge>
                )}
              </div>
            )}
          </div>

          <div className="flex items-center gap-1 sm:gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onComplete(task.id, !task.completed)}
              className="h-10 w-10 sm:h-8 sm:w-8 p-0"
              title={task.completed ? "Mark incomplete" : "Mark complete"}
            >
              {task.completed ? (
                <X className="h-5 w-5 sm:h-4 sm:w-4 text-gray-600" />
              ) : (
                <Check className="h-5 w-5 sm:h-4 sm:w-4 text-green-600" />
              )}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit(task)}
              className="h-10 w-10 sm:h-8 sm:w-8 p-0"
              title="Edit task"
            >
              <Edit className="h-5 w-5 sm:h-4 sm:w-4 text-blue-600" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(task.id)}
              className="h-10 w-10 sm:h-8 sm:w-8 p-0"
              title="Delete task"
            >
              <Trash2 className="h-5 w-5 sm:h-4 sm:w-4 text-red-600" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
