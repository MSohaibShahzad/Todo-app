/**
 * API type definitions
 */

export interface APIError {
  detail: string
  status_code?: number
}

export interface APIResponse<T> {
  data?: T
  error?: APIError
}
