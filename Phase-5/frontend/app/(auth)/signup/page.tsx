/**
 * Signup page with beautiful design
 */
"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { SignupForm } from "@/components/features/auth/SignupForm"
import Link from "next/link"
import { motion } from "framer-motion"

export default function SignupPage() {
  return (
    <Card className="bg-white/95 backdrop-blur-sm border-white/20 shadow-2xl hover:bg-white/95 hover:shadow-[0_20px_50px_rgba(6,182,212,0.3)]">
      <CardHeader>
        <CardTitle className="text-2xl bg-gradient-to-r from-[#06B6D4] to-[#10B981] bg-clip-text text-transparent">
          Create an account
        </CardTitle>
        <p className="text-sm text-gray-600">
          Enter your details to get started
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <SignupForm />
        <p className="text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link
            href="/login"
            className="text-[#06B6D4] hover:text-[#10B981] font-medium transition-colors"
          >
            Sign in
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
              className="w-full px-4 py-2 text-gray-600 hover:text-[#06B6D4] transition-colors text-sm"
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
