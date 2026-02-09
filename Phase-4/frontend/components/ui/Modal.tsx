/**
 * Modal component for dialogs
 * Enhanced with dark gradient theme, glass morphism effects, and smooth animations
 * Matches the modern design system with backdrop blur and gradient borders
 */
"use client"

import { cn } from "@/lib/utils/cn"
import { X } from "lucide-react"
import { useEffect } from "react"
import { Button } from "./Button"
import { motion, AnimatePresence } from "framer-motion"

export interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  className?: string
}

export function Modal({ isOpen, onClose, title, children, className }: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose()
    }

    if (isOpen) {
      document.addEventListener("keydown", handleEscape)
      document.body.style.overflow = "hidden"
    }

    return () => {
      document.removeEventListener("keydown", handleEscape)
      document.body.style.overflow = "unset"
    }
  }, [isOpen, onClose])

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center sm:p-4">
          {/* Animated Overlay with Backdrop Blur */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-md"
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Modal Container */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className={cn(
              "relative w-full h-full overflow-y-auto",
              "sm:rounded-2xl sm:max-w-lg sm:h-auto sm:max-h-[90vh]",
              "bg-gradient-to-br from-[#1A1F2E] via-[#232936] to-[#1A1F2E]",
              "border border-white/20 shadow-2xl",
              className
            )}
          >
            {/* Gradient glow effect */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-[#3B82F6] via-[#8B5CF6] to-[#06B6D4] opacity-10 blur-2xl" />

            {/* Header */}
            <div className="relative flex items-center justify-between p-5 sm:p-6 border-b border-white/10 bg-white/5 backdrop-blur-sm">
              <h2 className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">
                {title}
              </h2>
              <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClose}
                  className="h-9 w-9 p-0 hover:bg-white/10 hover:border-white/20 rounded-lg transition-all"
                >
                  <X className="h-5 w-5 text-white/70 hover:text-white" />
                </Button>
              </motion.div>
            </div>

            {/* Content */}
            <div className="relative p-5 sm:p-6 bg-white/[0.02] backdrop-blur-sm">
              {children}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
