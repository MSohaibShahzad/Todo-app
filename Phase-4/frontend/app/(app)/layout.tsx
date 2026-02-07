/**
 * Authenticated app layout with auth guard and new color scheme
 */
"use client"

import { UserMenu } from "@/components/features/auth/UserMenu"
import { LoadingSpinner } from "@/components/ui/LoadingSpinner"
import { useAuth } from "@/lib/hooks/useAuth"
import { useRouter, usePathname } from "next/navigation"
import { useEffect } from "react"
import Link from "next/link"
import { MessageSquare, CheckSquare } from "lucide-react"
import { motion } from "framer-motion"

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login")
    }
  }, [isAuthenticated, isLoading, router])

  if (isLoading) {
    return <LoadingSpinner fullScreen size="lg" />
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A0E1A] via-[#1A1F2E] to-[#232936]">
      <motion.header
        className="relative z-50 bg-[#1A1F2E]/80 backdrop-blur-sm shadow-lg border-b border-white/10"
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-6">
              <Link href="/" className="flex items-center gap-2 group">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#10B981] to-[#06B6D4] flex items-center justify-center group-hover:scale-110 transition-transform shadow-md shadow-[#10B981]/30">
                  <CheckSquare className="w-5 h-5 text-white" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xl font-bold bg-gradient-to-r from-[#10B981] to-[#06B6D4] bg-clip-text text-transparent">
                    Nexus
                  </span>
                  <span className="text-xs -mt-1 text-white/60">tasks</span>
                </div>
              </Link>
              <nav className="flex gap-2">
                <Link
                  href="/dashboard"
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                    pathname === "/dashboard"
                      ? "bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] text-white shadow-lg shadow-[#3B82F6]/30"
                      : "text-white/70 hover:bg-white/10"
                  }`}
                >
                  <CheckSquare className="w-4 h-4" />
                  Tasks
                </Link>
                <Link
                  href="/chat"
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                    pathname === "/chat"
                      ? "bg-gradient-to-r from-[#10B981] to-[#06B6D4] text-white shadow-lg shadow-[#10B981]/30"
                      : "text-white/70 hover:bg-white/10"
                  }`}
                >
                  <MessageSquare className="w-4 h-4" />
                  Chat
                </Link>
              </nav>
            </div>
            <UserMenu />
          </div>
        </div>
      </motion.header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {children}
        </motion.div>
      </main>
      <footer className="mt-auto py-6 border-t border-white/10 bg-[#1A1F2E]/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-white/70">
            Made with <span className="text-red-500">❤️</span> by{" "}
            <a
              href="https://github.com/MSohaibShahzad"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#10B981] hover:text-[#06B6D4] transition-colors font-medium"
            >
              Sohaib Shahzad
            </a>
          </p>
        </div>
      </footer>
    </div>
  )
}
