// Affiche la connexion ou l'accueil selon la session (SC-11).

import { useCallback, useState } from 'react'
import { loadSession, type Session } from './auth/session'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'

export default function App() {
  const [session, setSession] = useState<Session | null>(() => loadSession())
  const handleLoggedOut = useCallback(() => setSession(null), [])

  if (!session) return <LoginPage onLoggedIn={setSession} />
  return <HomePage session={session} onLoggedOut={handleLoggedOut} />
}
