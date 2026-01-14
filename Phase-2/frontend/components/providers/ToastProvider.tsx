/**
 * Client-side toast provider wrapper
 */
"use client"

import { ToastProvider as ToastProviderImpl } from "@/lib/hooks/useToast"
import type { ReactNode } from "react"

export function ToastProvider({ children }: { children: ReactNode }) {
  return <ToastProviderImpl>{children}</ToastProviderImpl>
}
