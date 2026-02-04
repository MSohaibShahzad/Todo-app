/**
 * Conversation and message types
 */

export interface Message {
  id: number
  conversation_id: number
  role: "user" | "assistant" | "system"
  content: string
  created_at: string
}

export interface ToolExecution {
  id: number
  tool_name: string
  parameters: Record<string, unknown>
  result?: Record<string, unknown> | null
  status: "pending" | "success" | "failed"
  error_message?: string | null
  created_at: string
}

export interface Conversation {
  id: number
  user_id: string
  title?: string | null
  is_active: boolean
  created_at: string
  updated_at: string
  messages?: Message[]
}

export interface ConversationCreate {
  title?: string
  initial_message?: string
}

export interface SendMessageRequest {
  content: string
}

export interface SendMessageResponse {
  user_message: Message
  assistant_message: Message
  tool_executions: ToolExecution[]
}
