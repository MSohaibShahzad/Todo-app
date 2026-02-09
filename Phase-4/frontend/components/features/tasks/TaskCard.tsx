/**
 * Task card component displaying individual task
 * Enhanced with gradient borders, glow effects, and smooth animations
 * Matches the modern dark gradient design system
 */
"use client"

import { Badge, PriorityBadge } from "@/components/ui/Badge"
import { Button } from "@/components/ui/Button"
import { Card, CardContent } from "@/components/ui/Card"
import { formatDueDate, isOverdue, isDueToday } from "@/lib/utils/date-formatting"
import type { Task } from "@/types/task"
import { Calendar, Check, Edit, Trash2, X, Sparkles } from "lucide-react"
import { motion } from "framer-motion"

export interface TaskCardProps {
  task: Task
  onComplete: (id: number, completed: boolean) => void
  onEdit: (task: Task) => void
  onDelete: (id: number) => void
}

export function TaskCard({ task, onComplete, onEdit, onDelete }: TaskCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ scale: 1.02, y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <Card
        className={`group relative overflow-hidden ${
          task.completed
            ? "opacity-60"
            : "hover:shadow-xl hover:shadow-[#3B82F6]/20"
        }`}
      >
        {/* Gradient border glow effect on hover */}
        <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-[#3B82F6] via-[#8B5CF6] to-[#06B6D4] opacity-0 group-hover:opacity-20 blur-xl transition-opacity duration-300" />

        <CardContent className="relative p-4 sm:p-5">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-3 flex-wrap">
                {/* Task ID Badge with gradient */}
                <Badge
                  variant="default"
                  size="sm"
                  className="bg-gradient-to-r from-[#3B82F6]/20 to-[#06B6D4]/20 text-[#06B6D4] font-mono border border-[#06B6D4]/30 backdrop-blur-sm"
                >
                  #{task.id}
                </Badge>

                {/* Task Title */}
                <h3
                  className={`font-semibold text-lg text-white ${
                    task.completed ? "line-through text-white/60" : ""
                  }`}
                >
                  {task.title}
                </h3>

                {/* Priority Badge */}
                <PriorityBadge priority={task.priority} />

                {/* Category Badge */}
                {task.category && (
                  <Badge
                    variant="default"
                    size="sm"
                    className="bg-[#8B5CF6]/20 text-[#8B5CF6] border border-[#8B5CF6]/30 backdrop-blur-sm"
                  >
                    <Sparkles className="h-3 w-3 mr-1" />
                    {task.category}
                  </Badge>
                )}
              </div>

              {/* Description */}
              {task.description && (
                <p className="text-sm text-white/80 mb-3 leading-relaxed">
                  {task.description}
                </p>
              )}

              {/* Due Date */}
              {task.due_date && (
                <div className="flex items-center gap-2 mt-2">
                  <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
                    <Calendar className="h-4 w-4 text-[#06B6D4]" />
                    <span className="text-sm text-white/90 font-medium">
                      {formatDueDate(task.due_date)}
                    </span>
                  </div>
                  {isOverdue(task.due_date, task.completed) && (
                    <Badge variant="danger" size="sm" className="animate-pulse">
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

            {/* Action Buttons */}
            <div className="flex items-center gap-1.5 sm:gap-2">
              <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onComplete(task.id, !task.completed)}
                  className={`h-10 w-10 sm:h-9 sm:w-9 p-0 rounded-lg transition-all ${
                    task.completed
                      ? "hover:bg-orange-500/20 hover:border-orange-400/30"
                      : "hover:bg-green-500/20 hover:border-green-400/30"
                  }`}
                  title={task.completed ? "Mark incomplete" : "Mark complete"}
                >
                  {task.completed ? (
                    <X className="h-5 w-5 sm:h-4 sm:w-4 text-orange-400" />
                  ) : (
                    <Check className="h-5 w-5 sm:h-4 sm:w-4 text-green-400" />
                  )}
                </Button>
              </motion.div>

              <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onEdit(task)}
                  className="h-10 w-10 sm:h-9 sm:w-9 p-0 hover:bg-[#3B82F6]/20 hover:border-[#3B82F6]/30 rounded-lg transition-all"
                  title="Edit task"
                >
                  <Edit className="h-5 w-5 sm:h-4 sm:w-4 text-[#3B82F6]" />
                </Button>
              </motion.div>

              <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onDelete(task.id)}
                  className="h-10 w-10 sm:h-9 sm:w-9 p-0 hover:bg-red-500/20 hover:border-red-400/30 rounded-lg transition-all"
                  title="Delete task"
                >
                  <Trash2 className="h-5 w-5 sm:h-4 sm:w-4 text-red-400" />
                </Button>
              </motion.div>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}
