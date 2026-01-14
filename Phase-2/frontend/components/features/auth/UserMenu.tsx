/**
 * User menu with sign-out functionality
 */
"use client"

import { Button } from "@/components/ui/Button"
import { logout } from "@/lib/hooks/useAuth"
import { LogOut } from "lucide-react"

export function UserMenu() {
  const handleSignOut = () => {
    logout()
  }

  return (
    <Button
      variant="ghost"
      onClick={handleSignOut}
      className="flex items-center gap-2"
    >
      <LogOut className="h-4 w-4" />
      <span>Sign Out</span>
    </Button>
  )
}
