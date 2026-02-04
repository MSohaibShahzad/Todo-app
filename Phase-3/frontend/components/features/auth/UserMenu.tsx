/**
 * User menu with profile and sign-out functionality
 */
"use client"

import { useState } from "react"
import { useAuth, logout } from "@/lib/hooks/useAuth"
import { LogOut } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

export function UserMenu() {
  const { user } = useAuth()
  const [isOpen, setIsOpen] = useState(false)

  const handleSignOut = () => {
    logout()
  }

  // Get user initials for avatar
  const getInitials = (name?: string | null, email?: string | null) => {
    if (name) {
      const nameParts = name.split(" ")
      if (nameParts.length >= 2) {
        return `${nameParts[0][0]}${nameParts[1][0]}`.toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
    }
    if (email) {
      return email.substring(0, 2).toUpperCase()
    }
    return "U"
  }

  const initials = getInitials(user?.name, user?.email)

  return (
    <div className="relative">
      {/* User Profile Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/10 transition-colors"
      >
        {/* Avatar */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#3B82F6] to-[#06B6D4] flex items-center justify-center text-white font-semibold text-sm shadow-md">
          {initials}
        </div>
        {/* User Name */}
        <div className="hidden sm:block text-left">
          <div className="text-sm font-medium text-white">
            {user?.name || "User"}
          </div>
          <div className="text-xs text-white/70 truncate max-w-[150px]">
            {user?.email}
          </div>
        </div>
      </button>

      {/* Dropdown Menu */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <div
              className="fixed inset-0 z-10"
              onClick={() => setIsOpen(false)}
            />
            {/* Dropdown */}
            <motion.div
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ duration: 0.15 }}
              className="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-20"
            >
              {/* User Info */}
              <div className="px-4 py-3 border-b border-gray-100">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#3B82F6] to-[#06B6D4] flex items-center justify-center text-white font-semibold shadow-md">
                    {initials}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-gray-900 truncate">
                      {user?.name || "User"}
                    </div>
                    <div className="text-xs text-gray-500 truncate">
                      {user?.email}
                    </div>
                  </div>
                </div>
              </div>

              {/* Menu Items */}
              <div className="py-1">
                <button
                  onClick={handleSignOut}
                  className="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <LogOut className="w-4 h-4 text-gray-500" />
                  <span>Sign Out</span>
                </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}
