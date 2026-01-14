/**
 * Signup form component with validation and toast notifications
 */
"use client"

import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { useToast } from "@/lib/hooks/useToast"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { signUp } from "@/lib/auth/client"

export function SignupForm() {
  const router = useRouter()
  const { showSuccess, showError } = useToast()
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const result = await signUp.email({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      })

      if (result.error) {
        throw new Error(result.error.message || "Signup failed")
      }

      showSuccess("Account created successfully! Redirecting...")
      router.push("/dashboard")
    } catch (err) {
      showError(err instanceof Error ? err.message : "Signup failed")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">

      <Input
        label="Name"
        type="text"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        required
        disabled={isLoading}
      />

      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        required
        disabled={isLoading}
      />

      <Input
        label="Password"
        type="password"
        value={formData.password}
        onChange={(e) =>
          setFormData({ ...formData, password: e.target.value })
        }
        required
        minLength={8}
        disabled={isLoading}
      />

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? "Creating account..." : "Sign up"}
      </Button>
    </form>
  )
}
