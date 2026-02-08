/**
 * LoadingSpinner - Animated loading component with custom color palette
 */
"use client"

import { motion } from "framer-motion"

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg"
  fullScreen?: boolean
}

export function LoadingSpinner({ size = "md", fullScreen = false }: LoadingSpinnerProps) {
  const sizes = {
    sm: "w-6 h-6",
    md: "w-12 h-12",
    lg: "w-16 h-16"
  }

  const dotSizes = {
    sm: "w-1.5 h-1.5",
    md: "w-3 h-3",
    lg: "w-4 h-4"
  }

  const containerVariants = {
    start: {
      transition: {
        staggerChildren: 0.1
      }
    },
    end: {
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const dotVariants = {
    start: {
      y: "0%",
      scale: 1
    },
    end: {
      y: "100%",
      scale: 1.2
    }
  }

  const dotTransition = {
    duration: 0.5,
    repeat: Infinity,
    repeatType: "reverse" as const,
    ease: "easeInOut" as const
  }

  const colors = ["#3B82F6", "#06B6D4", "#8B5CF6", "#10B981"]

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-[#0A0E1A] via-[#1A1F2E] to-[#232936]">
        <div className="text-center">
          <motion.div
            className={`${sizes[size]} flex justify-around mx-auto mb-4`}
            variants={containerVariants}
            initial="start"
            animate="end"
          >
            {colors.map((color, i) => (
              <motion.span
                key={i}
                className={`${dotSizes[size]} rounded-full`}
                style={{ backgroundColor: color }}
                variants={dotVariants}
                transition={dotTransition}
              />
            ))}
          </motion.div>
          <motion.p
            className="text-white text-lg font-medium"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            Loading your tasks...
          </motion.p>
        </div>
      </div>
    )
  }

  return (
    <motion.div
      className={`${sizes[size]} flex justify-around`}
      variants={containerVariants}
      initial="start"
      animate="end"
    >
      {colors.map((color, i) => (
        <motion.span
          key={i}
          className={`${dotSizes[size]} rounded-full`}
          style={{ backgroundColor: color }}
          variants={dotVariants}
          transition={dotTransition}
        />
      ))}
    </motion.div>
  )
}
