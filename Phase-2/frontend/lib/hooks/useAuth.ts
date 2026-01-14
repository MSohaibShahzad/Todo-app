/**
 * Authentication hooks using Better Auth
 */
"use client"

import { useSession, signOut } from "@/lib/auth/client"
import { useRouter } from "next/navigation"

export function useAuth() {
  const { data: session, isPending, error } = useSession()
  const router = useRouter()

  // Better Auth returns { user, session } in the data
  const isAuthenticated = !!(session?.user && session?.session)
  const isLoading = isPending
  const user = session?.user ?? null

  const handleSignOut = async () => {
    await signOut()
    router.push("/login")
    router.refresh()
  }

  return {
    isAuthenticated,
    isLoading,
    user,
    session,
    error,
    signOut: handleSignOut,
  }
}

export async function logout() {
  await signOut()
  window.location.href = "/login"
}
