/**
 * Signup page
 */
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { SignupForm } from "@/components/features/auth/SignupForm"
import Link from "next/link"

export default function SignupPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Create an account</CardTitle>
        <p className="text-sm text-gray-600">
          Enter your details to get started
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <SignupForm />
        <p className="text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-600 hover:underline">
            Sign in
          </Link>
        </p>
      </CardContent>
    </Card>
  )
}
