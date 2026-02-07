/**
 * Conversation API client functions
 */
import type {
  Conversation,
  ConversationCreate,
  SendMessageRequest,
  SendMessageResponse,
} from "@/types/conversation"
import { api } from "./client"

export async function createConversation(
  data: ConversationCreate
): Promise<Conversation> {
  return api.post<Conversation>("/api/v1/conversations", data)
}

export async function sendMessage(
  conversationId: number,
  data: SendMessageRequest
): Promise<SendMessageResponse> {
  return api.post<SendMessageResponse>(
    `/api/v1/conversations/${conversationId}/messages`,
    data
  )
}

export async function listConversations(): Promise<{
  conversations: Conversation[]
}> {
  return api.get<{ conversations: Conversation[] }>("/api/v1/conversations")
}

export async function getConversation(
  conversationId: number
): Promise<Conversation> {
  return api.get<Conversation>(`/api/v1/conversations/${conversationId}`)
}
