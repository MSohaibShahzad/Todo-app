/**
 * Task API client functions
 */
import type { Task, TaskCreate, TaskUpdate } from "@/types/task"
import { api } from "./client"

export async function getTasks(): Promise<Task[]> {
  return api.get<Task[]>("/api/v1/tasks")
}

export async function getTask(id: number): Promise<Task> {
  return api.get<Task>(`/api/v1/tasks/${id}`)
}

export async function createTask(data: TaskCreate): Promise<Task> {
  return api.post<Task>("/api/v1/tasks", data)
}

export async function updateTask(
  id: number,
  data: TaskUpdate
): Promise<Task> {
  return api.put<Task>(`/api/v1/tasks/${id}`, data)
}

export async function deleteTask(id: number): Promise<void> {
  return api.delete<void>(`/api/v1/tasks/${id}`)
}

export async function toggleTaskComplete(
  id: number,
  completed: boolean
): Promise<Task> {
  return api.patch<Task>(`/api/v1/tasks/${id}/complete?completed=${completed}`, {})
}
