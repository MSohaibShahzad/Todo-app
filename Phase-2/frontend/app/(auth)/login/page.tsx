/**
 * Login page
 */
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { LoginForm } from "@/components/features/auth/LoginForm"
import Link from "next/link"

export default function LoginPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome back</CardTitle>
        <p className="text-sm text-gray-600">
          Sign in to your account to continue
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <LoginForm />
        <p className="text-center text-sm text-gray-600">
          Don&apos;t have an account?{" "}
          <Link href="/signup" className="text-blue-600 hover:underline">
            Sign up
          </Link>
        </p>
      </CardContent>
    </Card>
  )
}
