/**
 * Authentication layout with centered design and beautiful gradients
 */
"use client"

import { motion } from "framer-motion"
import { CheckSquare } from "lucide-react"
import Link from "next/link"

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0A0E1A] via-[#1A1F2E] to-[#232936] py-12 px-4 sm:px-6 lg:px-8 overflow-hidden relative">
      {/* Animated Background Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute w-96 h-96 rounded-full bg-[#8B5CF6] opacity-25 blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, -100, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{ duration: 20, repeat: Infinity }}
          style={{ top: "10%", left: "10%" }}
        />
        <motion.div
          className="absolute w-96 h-96 rounded-full bg-[#06B6D4] opacity-30 blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, 100, 0],
            scale: [1, 1.3, 1],
          }}
          transition={{ duration: 25, repeat: Infinity }}
          style={{ bottom: "10%", right: "10%" }}
        />
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo/Header */}
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Link href="/" className="inline-flex items-center gap-2 mb-2">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#3B82F6] to-[#06B6D4] flex items-center justify-center shadow-xl shadow-[#3B82F6]/40">
              <CheckSquare className="w-7 h-7 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-3xl font-bold text-white">Nexus</span>
              <span className="text-sm -mt-1 text-white/80">tasks</span>
            </div>
          </Link>
          <p className="text-white/80 text-sm">Your intelligent task management system</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          {children}
        </motion.div>

        {/* Footer */}
        <motion.div
          className="mt-8 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <p className="text-white/60 text-sm">
            Made with <span className="text-red-500">❤️</span> by{" "}
            <a
              href="https://github.com/MSohaibShahzad"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#06B6D4] hover:text-[#10B981] transition-colors font-medium"
            >
              Sohaib Shahzad
            </a>
          </p>
        </motion.div>
      </div>
    </div>
  )
}
