/**
 * SWR hook for task data fetching and caching
 */
"use client"

import { getTasks } from "@/lib/api/tasks"
import type { Task } from "@/types/task"
import useSWR from "swr"

export function useTasks() {
  const { data, error, isLoading, mutate } = useSWR<Task[]>(
    "/api/v1/tasks",
    getTasks,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  )

  return {
    tasks: data || [],
    isLoading,
    isError: error,
    mutate,
  }
}
