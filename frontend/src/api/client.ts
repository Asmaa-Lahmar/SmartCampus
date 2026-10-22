// Appels à l'API SmartCampus (SC-11). En développement, Vite relaie /api vers le port 8000.

import type { Session } from '../auth/session'

export class ApiError extends Error {
  status: number
  detail: string | null

  constructor(status: number, detail: string | null) {
    super(detail ?? `Erreur HTTP ${status}`)
    this.status = status
    this.detail = detail
  }
}

async function readError(response: Response): Promise<ApiError> {
  let detail: string | null = null
  try {
    const body = await response.json()
    if (typeof body?.detail === 'string') detail = body.detail
  } catch {
    // réponse sans JSON
  }
  return new ApiError(response.status, detail)
}

export async function login(email: string, password: string): Promise<Session> {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!response.ok) throw await readError(response)
  const body = await response.json()
  return { accessToken: body.access_token, expiresAt: body.expires_at, user: body.user }
}
