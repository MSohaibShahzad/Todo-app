/**
 * Chat page for conversational task management
 */
"use client"

import ChatInterface from "@/components/chat/ChatInterface"
import { motion } from "framer-motion"
import { useEffect, useState } from "react"

export default function ChatPage() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A0E1A] via-[#1A1F2E] to-[#232936] -m-6 p-6">
      {/* Animated Background Blobs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute w-96 h-96 rounded-full bg-[#8B5CF6] opacity-20 blur-3xl"
          animate={{
            x: mousePosition.x / 20,
            y: mousePosition.y / 20,
            scale: [1, 1.2, 1],
          }}
          transition={{ duration: 3, repeat: Infinity }}
          style={{ top: "10%", left: "10%" }}
        />
        <motion.div
          className="absolute w-96 h-96 rounded-full bg-[#06B6D4] opacity-30 blur-3xl"
          animate={{
            x: -mousePosition.x / 30,
            y: -mousePosition.y / 30,
            scale: [1, 1.3, 1],
          }}
          transition={{ duration: 4, repeat: Infinity }}
          style={{ bottom: "10%", right: "10%" }}
        />
      </div>

      <div className="relative z-10 container mx-auto max-w-4xl">
        <motion.div
          className="mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <motion.div
              className="w-12 h-12 rounded-xl bg-gradient-to-r from-[#10B981] to-[#06B6D4] flex items-center justify-center"
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.6 }}
            >
              <span className="text-white font-bold text-lg">AI</span>
            </motion.div>
            Task Assistant
          </h1>
          <p className="text-white/70 mt-2">
            Manage your tasks through natural conversation
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <ChatInterface/>
        </motion.div>
      </div>
    </div>
  )
}
