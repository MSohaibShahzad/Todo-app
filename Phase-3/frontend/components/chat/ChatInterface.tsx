"use client"

/**
 * Chat interface component using OpenAI ChatKit with custom backend
 */
import { useChatKit, ChatKit } from "@openai/chatkit-react"
import { useEffect, useState } from "react"
import { getJWTToken } from "@/lib/auth/client"

export default function ChatInterface() {
  const [debugInfo, setDebugInfo] = useState("Initializing ChatKit...")

  // Initialize ChatKit with custom backend server
  // For custom backends, use url + domainKey pattern
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const domainKey = process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY || 'local-dev'

  const { control } = useChatKit({
    api: {
      url: `${apiUrl}/api/v1/chatkit`,
      domainKey, // Read from environment variable
      fetch: async (input, init) => {
        // Get JWT token using the proper auth function
        const jwtToken = await getJWTToken()
        if (!jwtToken) {
          throw new Error('No JWT token found. Please log in again.')
        }

        // Add Authorization header
        const headers = new Headers(init?.headers)
        headers.set('Authorization', `Bearer ${jwtToken}`)

        return fetch(input, {
          ...init,
          headers,
          credentials: 'include',
        })
      },
    },
    onReady: () => {
      console.log("[ChatKit] Ready")
    },
    onError: ({ error }) => {
      console.error("[ChatKit] Error:", error)
    },
    onResponseStart: () => {
      console.log("[ChatKit] Response started")
    },
    onResponseEnd: () => {
      console.log("[ChatKit] Response ended")
    },
  })

  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden bg-gradient-to-br from-[#1A1F2E] to-[#232936] border border-white/10 shadow-2xl">
      <ChatKit
        control={control}
        className="h-full w-full"
      />
    </div>
  )
}
