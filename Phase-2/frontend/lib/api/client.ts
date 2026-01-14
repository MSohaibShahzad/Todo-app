/**
 * Base API client with authentication and error handling
 *
 * Uses relative URLs to leverage Next.js proxy (next.config.ts rewrites)
 * All /api/v1/* requests are automatically proxied to backend
 */
import type { APIError } from "@/types/api"
import { getJWTToken } from "@/lib/auth/client"

// Use empty string for relative URLs - Next.js will proxy /api/v1/* to backend
const API_URL = ""

export class APIClient {
  private baseURL: string

  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL
  }

  private async getAuthToken(): Promise<string | null> {
    return await getJWTToken()
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getAuthToken()
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    }

    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      if (response.status === 401) {
        // Redirect to login on unauthorized
        if (typeof window !== "undefined") {
          window.location.href = "/login"
        }
      }

      const error: APIError = await response.json()
      throw new Error(error.detail || "An error occurred")
    }

    // Handle 204 No Content responses (e.g., DELETE)
    if (response.status === 204) {
      return undefined as T
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "GET" })
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PATCH",
      body: JSON.stringify(data),
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "DELETE" })
  }
}

export const api = new APIClient()
