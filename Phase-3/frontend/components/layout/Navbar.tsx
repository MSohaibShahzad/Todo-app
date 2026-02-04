/**
 * Navbar - Beautiful navigation bar for landing page
 */
"use client"

import { motion } from "framer-motion"
import { CheckSquare } from "lucide-react"
import Link from "next/link"
import { useAuth } from "@/lib/hooks/useAuth"
import { UserMenu } from "@/components/features/auth/UserMenu"

interface NavbarProps {
  transparent?: boolean
}

export function Navbar({ transparent = false }: NavbarProps) {
  const { isAuthenticated } = useAuth()
  return (
    <motion.nav
      className={`fixed top-0 left-0 right-0 z-50 ${
        transparent
          ? "bg-transparent"
          : "bg-white/80 backdrop-blur-md border-b border-gray-200"
      }`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#3B82F6] to-[#8B5CF6] flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg shadow-[#3B82F6]/30">
              <CheckSquare className="w-6 h-6 text-white" />
            </div>
            <div className="flex flex-col">
              <span className={`text-xl font-bold ${transparent ? "text-white" : "bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] bg-clip-text text-transparent"}`}>
                Nexus
              </span>
              <span className={`text-xs -mt-1 ${transparent ? "text-white/80" : "text-gray-600"}`}>
                tasks
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center gap-8">
            <Link
              href="#features"
              className={`text-sm font-medium transition-colors ${
                transparent
                  ? "text-white/90 hover:text-white"
                  : "text-gray-700 hover:text-[#3B82F6]"
              }`}
            >
              Features
            </Link>
            <Link
              href="#about"
              className={`text-sm font-medium transition-colors ${
                transparent
                  ? "text-white/90 hover:text-white"
                  : "text-gray-700 hover:text-[#3B82F6]"
              }`}
            >
              About
            </Link>
            <Link
              href="/dashboard"
              className={`text-sm font-medium transition-colors ${
                transparent
                  ? "text-white/90 hover:text-white"
                  : "text-gray-700 hover:text-[#3B82F6]"
              }`}
            >
              Dashboard
            </Link>
          </div>

          {/* Auth Buttons */}
          <div className="flex gap-3">
            {isAuthenticated ? (
              <UserMenu />
            ) : (
              <>
                <Link href="/login">
                  <motion.button
                    className={`px-5 py-2 text-sm font-medium rounded-lg transition-colors ${
                      transparent
                        ? "text-white hover:bg-white/10"
                        : "text-gray-700 hover:bg-gray-100"
                    }`}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Login
                  </motion.button>
                </Link>
                <Link href="/signup">
                  <motion.button
                    className="px-5 py-2 text-sm font-medium bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] text-white rounded-lg hover:shadow-xl hover:shadow-[#3B82F6]/50 transition-all hover:scale-105"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Get Started
                  </motion.button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </motion.nav>
  )
}
