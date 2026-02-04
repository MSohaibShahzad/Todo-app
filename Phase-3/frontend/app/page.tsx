/**
 * Landing Page - Beautiful intro with animations
 */
"use client"

import { motion } from "framer-motion"
import { CheckCircle2, Zap, Calendar, BarChart3, ArrowRight } from "lucide-react"
import { Navbar } from "@/components/layout/Navbar"
import { Footer } from "@/components/layout/Footer"
import Link from "next/link"
import { useState, useEffect } from "react"
import { useAuth } from "@/lib/hooks/useAuth"

export default function Home() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const { isAuthenticated } = useAuth()

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  const features = [
    {
      icon: CheckCircle2,
      title: "Smart Task Management",
      description: "Organize your tasks with priorities, categories, and smart filtering",
      color: "#3B82F6"
    },
    {
      icon: Calendar,
      title: "Due Date Tracking",
      description: "Never miss a deadline with intelligent reminders and overdue alerts",
      color: "#8B5CF6"
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Built with Next.js and FastAPI for blazing fast performance",
      color: "#06B6D4"
    },
    {
      icon: BarChart3,
      title: "Progress Analytics",
      description: "Track your productivity with beautiful stats and insights",
      color: "#10B981"
    }
  ]

  const stats = [
    { value: "100%", label: "Free Forever" },
    { value: "∞", label: "Unlimited Tasks" },
    { value: "⚡", label: "Real-time Sync" },
    { value: "🔒", label: "Secure & Private" }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A0E1A] via-[#1A1F2E] to-[#232936] overflow-hidden relative">
      {/* Animated Background Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
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

      <div className="relative z-10">
        {/* Navbar */}
        <Navbar transparent />

        {/* Hero Section */}
        <section className="container mx-auto px-6 py-32 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <motion.div
              className="inline-block mb-6"
              animate={{ rotate: [0, 5, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <span className="inline-block px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-[#06B6D4] text-sm font-medium border border-white/20">
                ✨ Your Personal Productivity Companion
              </span>
            </motion.div>

            <h2 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
              Manage Tasks
              <br />
              <span className="bg-gradient-to-r from-[#3B82F6] to-[#06B6D4] bg-clip-text text-transparent">
                Like Never Before
              </span>
            </h2>

            <p className="text-xl text-white/80 mb-12 max-w-2xl mx-auto">
              Experience the future of task management with our beautifully designed,
              lightning-fast app. Stay organized, focused, and productive.
            </p>

            <div className="flex gap-4 justify-center flex-wrap">
              <Link href={isAuthenticated ? "/dashboard" : "/signup"}>
                <motion.button
                  className="px-8 py-4 bg-gradient-to-r from-[#3B82F6] to-[#06B6D4] text-white rounded-xl font-semibold text-lg flex items-center gap-2 hover:shadow-2xl hover:shadow-[#3B82F6]/50 transition-all"
                  whileHover={{ scale: 1.05, y: -3 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {isAuthenticated ? "Go to Dashboard" : "Start Free Now"}
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
              {!isAuthenticated && (
                <Link href="/dashboard">
                  <motion.button
                    className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white rounded-xl font-semibold text-lg border border-white/20 hover:bg-white/20 hover:border-[#3B82F6] transition-all"
                    whileHover={{ scale: 1.05, y: -3 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    View Demo
                  </motion.button>
                </Link>
              )}
            </div>

            {/* Animated Illustration */}
            <motion.div
              className="mt-20 relative"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.5 }}
            >
              <div className="relative mx-auto max-w-4xl">
                {/* Floating Task Cards */}
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    className="absolute bg-white rounded-xl shadow-2xl p-4"
                    style={{
                      left: `${20 + i * 30}%`,
                      top: `${i * 20}px`,
                    }}
                    animate={{
                      y: [0, -20, 0],
                      rotate: [0, 2, -2, 0],
                    }}
                    transition={{
                      duration: 3 + i,
                      repeat: Infinity,
                      delay: i * 0.2,
                    }}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-4 h-4 rounded-full bg-[#3B82F6]" />
                      <div className="h-2 bg-gray-200 rounded w-32" />
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </motion.div>
        </section>

        {/* Stats Section */}
        <section className="container mx-auto px-6 py-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                className="text-center p-6 bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-sm rounded-xl border border-white/20 hover:border-[#3B82F6]/50 transition-all"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05, y: -5 }}
              >
                <div className="text-4xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-white/70">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h3 className="text-4xl font-bold text-white mb-4">
              Powerful Features for You
            </h3>
            <p className="text-white/70 text-lg">
              Everything you need to stay productive and organized
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                className="p-6 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 hover:bg-white/10 hover:border-[#3B82F6]/50 transition-all group"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10, scale: 1.02 }}
              >
                <motion.div
                  className="w-12 h-12 rounded-xl flex items-center justify-center mb-4"
                  style={{ backgroundColor: feature.color }}
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.6 }}
                >
                  <feature.icon className="w-6 h-6 text-white" />
                </motion.div>
                <h4 className="text-xl font-semibold text-white mb-2">
                  {feature.title}
                </h4>
                <p className="text-white/70">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* AI Agent Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-md rounded-3xl p-12 border border-white/20"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <motion.div
                  className="inline-block mb-4"
                  initial={{ scale: 0 }}
                  whileInView={{ scale: 1 }}
                  viewport={{ once: true }}
                >
                  <span className="px-4 py-2 bg-gradient-to-r from-[#8B5CF6] to-[#3B82F6] text-white rounded-full text-sm font-medium">
                    🤖 AI-Powered
                  </span>
                </motion.div>
                <h3 className="text-4xl font-bold text-white mb-6">
                  Meet Your AI Task Assistant
                </h3>
                <p className="text-white/80 text-lg mb-6">
                  Our intelligent AI agent can manage your entire task workflow through natural conversation. Just chat with it!
                </p>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-[#10B981] flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-white text-lg">✓</span>
                    </div>
                    <div>
                      <h4 className="text-white font-semibold mb-1">Add Tasks Naturally</h4>
                      <p className="text-white/70 text-sm">Just say "Add a task to buy groceries tomorrow" and it's done!</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-[#06B6D4] flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-white text-lg">✓</span>
                    </div>
                    <div>
                      <h4 className="text-white font-semibold mb-1">Update & Edit Tasks</h4>
                      <p className="text-white/70 text-sm">Modify tasks by chatting: "Change the deadline to next Friday"</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-[#8B5CF6] flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-white text-lg">✓</span>
                    </div>
                    <div>
                      <h4 className="text-white font-semibold mb-1">Smart Management</h4>
                      <p className="text-white/70 text-sm">Ask "What's due today?" or "Complete all high priority tasks"</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-[#3B82F6] flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-white text-lg">✓</span>
                    </div>
                    <div>
                      <h4 className="text-white font-semibold mb-1">Everything by Voice</h4>
                      <p className="text-white/70 text-sm">Add, edit, update, delete - all through conversational AI</p>
                    </div>
                  </div>
                </div>
                <Link href="/chat">
                  <motion.button
                    className="mt-8 px-8 py-4 bg-gradient-to-r from-[#10B981] to-[#06B6D4] text-white rounded-xl font-semibold text-lg hover:shadow-2xl hover:shadow-[#10B981]/50 transition-all flex items-center gap-2"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Try AI Assistant
                    <ArrowRight className="w-5 h-5" />
                  </motion.button>
                </Link>
              </div>
              <div className="relative">
                <motion.div
                  className="bg-gradient-to-br from-[#232936] to-[#1A1F2E] rounded-2xl p-6 shadow-2xl border border-white/10 max-h-[600px] overflow-hidden"
                  initial={{ opacity: 0, x: 50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.2 }}
                >
                  {/* Chat Header */}
                  <div className="flex items-center gap-3 pb-4 border-b border-white/10 mb-4">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-r from-[#10B981] to-[#06B6D4] flex items-center justify-center">
                      <span className="text-white font-bold text-lg">AI</span>
                    </div>
                    <div>
                      <h4 className="text-white font-semibold">Task Assistant</h4>
                      <div className="flex items-center gap-1">
                        <div className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse" />
                        <span className="text-xs text-white/60">Online</span>
                      </div>
                    </div>
                  </div>

                  {/* Chat Messages */}
                  <div className="space-y-3 overflow-y-auto max-h-[480px]">
                    {/* Message 1 - User (starts immediately) */}
                    <motion.div
                      className="flex gap-3"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.5, duration: 0.4 }}
                    >
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] flex-shrink-0 flex items-center justify-center">
                        <span className="text-white text-xs font-bold">You</span>
                      </div>
                      <div className="flex-1">
                        <div className="bg-white/10 rounded-2xl rounded-tl-sm p-3 text-white/90 text-sm">
                          Add a task to finish the project report by Friday with high priority
                        </div>
                      </div>
                    </motion.div>

                    {/* Message 2 - AI Response (3 sec after user message) */}
                    <motion.div
                      className="flex gap-3 justify-end"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 3.5, duration: 0.4 }}
                    >
                      <div className="flex-1 flex justify-end">
                        <div className="bg-gradient-to-r from-[#10B981] to-[#06B6D4] rounded-2xl rounded-tr-sm p-3 text-white text-sm max-w-[85%]">
                          ✓ Task created successfully!<br/>
                          <span className="text-xs opacity-90">📝 "Finish project report" | Due: Friday | Priority: High</span>
                        </div>
                      </div>
                    </motion.div>

                    {/* Message 3 - User (4 sec after AI response) */}
                    <motion.div
                      className="flex gap-3"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 7.5, duration: 0.4 }}
                    >
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] flex-shrink-0 flex items-center justify-center">
                        <span className="text-white text-xs font-bold">You</span>
                      </div>
                      <div className="flex-1">
                        <div className="bg-white/10 rounded-2xl rounded-tl-sm p-3 text-white/90 text-sm">
                          What tasks are due this week?
                        </div>
                      </div>
                    </motion.div>

                    {/* Message 4 - AI Response (3 sec after user) */}
                    <motion.div
                      className="flex gap-3 justify-end"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 10.5, duration: 0.4 }}
                    >
                      <div className="flex-1 flex justify-end">
                        <div className="bg-gradient-to-r from-[#10B981] to-[#06B6D4] rounded-2xl rounded-tr-sm p-3 text-white text-sm max-w-[85%]">
                          You have 3 tasks due this week:<br/>
                          <span className="text-xs opacity-90">
                            1. 🔴 Finish project report - Friday<br/>
                            2. 🟡 Team meeting prep - Wednesday<br/>
                            3. 🟢 Code review - Thursday
                          </span>
                        </div>
                      </div>
                    </motion.div>

                    {/* Message 5 - User (5 sec after AI) */}
                    <motion.div
                      className="flex gap-3"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 15.5, duration: 0.4 }}
                    >
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] flex-shrink-0 flex items-center justify-center">
                        <span className="text-white text-xs font-bold">You</span>
                      </div>
                      <div className="flex-1">
                        <div className="bg-white/10 rounded-2xl rounded-tl-sm p-3 text-white/90 text-sm">
                          Change the project report deadline to next Monday
                        </div>
                      </div>
                    </motion.div>

                    {/* Message 6 - AI Response (2 sec after user) */}
                    <motion.div
                      className="flex gap-3 justify-end"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 17.5, duration: 0.4 }}
                    >
                      <div className="flex-1 flex justify-end">
                        <div className="bg-gradient-to-r from-[#10B981] to-[#06B6D4] rounded-2xl rounded-tr-sm p-3 text-white text-sm max-w-[85%]">
                          ✓ Updated!<br/>
                          <span className="text-xs opacity-90">📝 "Finish project report" deadline changed to Monday</span>
                        </div>
                      </div>
                    </motion.div>

                    {/* Message 7 - User (4 sec after AI) */}
                    <motion.div
                      className="flex gap-3"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 21.5, duration: 0.4 }}
                    >
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] flex-shrink-0 flex items-center justify-center">
                        <span className="text-white text-xs font-bold">You</span>
                      </div>
                      <div className="flex-1">
                        <div className="bg-white/10 rounded-2xl rounded-tl-sm p-3 text-white/90 text-sm">
                          Mark team meeting prep as complete
                        </div>
                      </div>
                    </motion.div>

                    {/* Message 8 - AI Response (2 sec after user) */}
                    <motion.div
                      className="flex gap-3 justify-end"
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 23.5, duration: 0.4 }}
                    >
                      <div className="flex-1 flex justify-end">
                        <div className="bg-gradient-to-r from-[#10B981] to-[#06B6D4] rounded-2xl rounded-tr-sm p-3 text-white text-sm max-w-[85%]">
                          ✓ Completed!<br/>
                          <span className="text-xs opacity-90">✅ "Team meeting prep" marked as done. Great work!</span>
                        </div>
                      </div>
                    </motion.div>

                    {/* Typing Indicator (appears after last message) */}
                    <motion.div
                      className="flex gap-3"
                      initial={{ opacity: 0 }}
                      whileInView={{ opacity: [0, 1, 1, 0] }}
                      viewport={{ once: true }}
                      transition={{ delay: 27.5, duration: 2, repeat: Infinity, repeatDelay: 1 }}
                    >
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] flex-shrink-0 flex items-center justify-center">
                        <span className="text-white text-xs font-bold">You</span>
                      </div>
                      <div className="flex-1">
                        <div className="bg-white/10 rounded-2xl rounded-tl-sm p-3 flex gap-1">
                          <motion.div
                            className="w-2 h-2 rounded-full bg-white/60"
                            animate={{ scale: [1, 1.5, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0 }}
                          />
                          <motion.div
                            className="w-2 h-2 rounded-full bg-white/60"
                            animate={{ scale: [1, 1.5, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0.2 }}
                          />
                          <motion.div
                            className="w-2 h-2 rounded-full bg-white/60"
                            animate={{ scale: [1, 1.5, 1] }}
                            transition={{ repeat: Infinity, duration: 1, delay: 0.4 }}
                          />
                        </div>
                      </div>
                    </motion.div>
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            className="relative bg-gradient-to-br from-[#06B6D4] via-[#3B82F6] to-[#8B5CF6] rounded-3xl p-12 text-center shadow-2xl shadow-[#06B6D4]/30 overflow-hidden"
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
          >
            {/* Animated background effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-[#10B981]/20 to-transparent animate-pulse-glow" />

            <div className="relative z-10">
              <h3 className="text-4xl font-bold text-white mb-4">
                {isAuthenticated ? "Continue Your Productivity Journey!" : "Ready to Boost Your Productivity?"}
              </h3>
              <p className="text-white/95 text-lg mb-8 max-w-2xl mx-auto">
                {isAuthenticated
                  ? "Your tasks are waiting for you. Let's get things done!"
                  : "Join thousands of users who are already managing their tasks smarter, not harder."
                }
              </p>
              <Link href={isAuthenticated ? "/dashboard" : "/signup"}>
                <motion.button
                  className="px-10 py-4 bg-white text-[#0A0E1A] rounded-xl font-bold text-lg shadow-xl hover:shadow-2xl hover:bg-gradient-to-r hover:from-[#10B981] hover:to-[#06B6D4] hover:text-white transition-all"
                  whileHover={{ scale: 1.08, y: -5 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {isAuthenticated ? "Go to Dashboard" : "Get Started - It's Free"}
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </section>

      </div>

      {/* Footer */}
      <Footer variant="dark" />
    </div>
  )
}
