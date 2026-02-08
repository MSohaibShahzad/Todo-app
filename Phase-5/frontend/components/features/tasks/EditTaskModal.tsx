/**
 * Modal for editing existing tasks
 * Added toast notifications for success/error feedback
 */
"use client"

import { Modal } from "@/components/ui/Modal"
import { updateTask } from "@/lib/api/tasks"
import { useToast } from "@/lib/hooks/useToast"
import type { Task, TaskCreate } from "@/types/task"
import { useState } from "react"
import { TaskForm } from "./TaskForm"

export interface EditTaskModalProps {
  isOpen: boolean
  task: Task | null
  onClose: () => void
  onSuccess: () => void
  existingCategories?: string[]
}

export function EditTaskModal({
  isOpen,
  task,
  onClose,
  onSuccess,
  existingCategories = [],
}: EditTaskModalProps) {
  const [isLoading, setIsLoading] = useState(false)
  const { showSuccess, showError } = useToast()

  const handleSubmit = async (data: TaskCreate) => {
    if (!task) return

    setIsLoading(true)

    try {
      await updateTask(task.id, data)
      onSuccess()
      onClose()
      showSuccess("Task updated successfully")
    } catch (err) {
      console.error("Failed to update task:", err)
      showError(err instanceof Error ? err.message : "Failed to update task")
    } finally {
      setIsLoading(false)
    }
  }

  if (!task) return null

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Edit Task">
      <TaskForm
        initialData={task}
        onSubmit={handleSubmit}
        onCancel={onClose}
        isLoading={isLoading}
        existingCategories={existingCategories}
      />
    </Modal>
  )
}
