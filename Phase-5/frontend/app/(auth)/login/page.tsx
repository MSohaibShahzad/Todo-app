/**
 * Login page with beautiful design
 */
"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { LoginForm } from "@/components/features/auth/LoginForm"
import Link from "next/link"
import { motion } from "framer-motion"

export default function LoginPage() {
  return (
    <Card className="bg-white/95 backdrop-blur-sm border-white/20 shadow-2xl hover:bg-white/95 hover:shadow-[0_20px_50px_rgba(59,130,246,0.3)]">
      <CardHeader>
        <CardTitle className="text-2xl bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] bg-clip-text text-transparent">
          Welcome back
        </CardTitle>
        <p className="text-sm text-gray-600">
          Sign in to your account to continue
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <LoginForm />
        <p className="text-center text-sm text-gray-600">
          Don&apos;t have an account?{" "}
          <Link
            href="/signup"
            className="text-[#3B82F6] hover:text-[#8B5CF6] font-medium transition-colors"
          >
            Sign up
          </Link>
        </p>
        <motion.div
          className="pt-4 border-t border-gray-200"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <Link href="/">
            <motion.button
              className="w-full px-4 py-2 text-gray-600 hover:text-[#3B82F6] transition-colors text-sm"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              ← Back to home
            </motion.button>
          </Link>
        </motion.div>
      </CardContent>
    </Card>
  )
}
