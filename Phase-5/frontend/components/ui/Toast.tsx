/**
 * Toast notification component for displaying errors and success messages
 */
"use client"

import { AlertCircle, CheckCircle, Info, X, XCircle } from "lucide-react"
import { useEffect } from "react"

export type ToastType = "success" | "error" | "info" | "warning"

export interface ToastProps {
  message: string
  type?: ToastType
  onClose: () => void
  duration?: number
}

const icons = {
  success: CheckCircle,
  error: XCircle,
  info: Info,
  warning: AlertCircle,
}

const colors = {
  success: "bg-green-50 border-green-200 text-green-800",
  error: "bg-red-50 border-red-200 text-red-800",
  info: "bg-blue-50 border-blue-200 text-blue-800",
  warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
}

const iconColors = {
  success: "text-green-600",
  error: "text-red-600",
  info: "text-blue-600",
  warning: "text-yellow-600",
}

export function Toast({
  message,
  type = "info",
  onClose,
  duration = 5000,
}: ToastProps) {
  const Icon = icons[type]

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(onClose, duration)
      return () => clearTimeout(timer)
    }
  }, [duration, onClose])

  return (
    <div
      className={`fixed top-4 right-4 z-50 flex items-center gap-3 p-4 border rounded-lg shadow-lg max-w-md animate-slide-in ${colors[type]}`}
    >
      <Icon className={`h-5 w-5 flex-shrink-0 ${iconColors[type]}`} />
      <p className="text-sm flex-1">{message}</p>
      <button
        onClick={onClose}
        className="flex-shrink-0 hover:opacity-70 transition-opacity"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  )
}
