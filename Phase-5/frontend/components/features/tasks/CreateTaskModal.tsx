/**
 * Modal for creating new tasks
 * Added toast notifications for success/error feedback
 */
"use client"

import { Modal } from "@/components/ui/Modal"
import { createTask } from "@/lib/api/tasks"
import { useToast } from "@/lib/hooks/useToast"
import type { TaskCreate } from "@/types/task"
import { useState } from "react"
import { TaskForm } from "./TaskForm"

export interface CreateTaskModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
  existingCategories?: string[]
}

export function CreateTaskModal({
  isOpen,
  onClose,
  onSuccess,
  existingCategories = [],
}: CreateTaskModalProps) {
  const [isLoading, setIsLoading] = useState(false)
  const { showSuccess, showError } = useToast()

  const handleSubmit = async (data: TaskCreate) => {
    setIsLoading(true)

    try {
      await createTask(data)
      onSuccess()
      onClose()
      showSuccess("Task created successfully")
    } catch (err) {
      console.error("Failed to create task:", err)
      showError(err instanceof Error ? err.message : "Failed to create task")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Task">
      <TaskForm
        onSubmit={handleSubmit}
        onCancel={onClose}
        isLoading={isLoading}
        existingCategories={existingCategories}
      />
    </Modal>
  )
}
