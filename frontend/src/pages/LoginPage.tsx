// Écran de connexion (SC-11 : EF-AUTH-01, EF-AUTH-03).

import { useState, type FormEvent } from 'react'
import { ApiError, login } from '../api/client'
import { saveSession, type Session } from '../auth/session'

const INVALID_CREDENTIALS = 'E-mail ou mot de passe incorrect'
const SERVER_UNREACHABLE = 'Serveur injoignable. Réessayez dans un instant.'

interface Props {
  onLoggedIn: (session: Session) => void
}

export default function LoginPage({ onLoggedIn }: Props) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)
    setBusy(true)
    try {
      const session = await login(email, password)
      saveSession(session)
      onLoggedIn(session)
    } catch (err) {
      if (err instanceof ApiError && err.status >= 500) {
        setError(SERVER_UNREACHABLE)
      } else if (err instanceof ApiError) {
        // 400 : adresse hors domaine ; 403 : compte désactivé
        if ((err.status === 400 || err.status === 403) && err.detail) setError(err.detail)
        else setError(INVALID_CREDENTIALS)
      } else {
        setError(SERVER_UNREACHABLE)
      }
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="login-page">
      <form className="login-card" onSubmit={handleSubmit} noValidate>
        <div className="login-brand">
          <img src="/favicon.svg" alt="" width={40} height={40} />
          <div>
            <h1>SmartCampus</h1>
            <p>ENSA Khouribga</p>
          </div>
        </div>
        <h2>Connexion</h2>

        <label htmlFor="email">E-mail institutionnel</label>
        <input
          id="email"
          type="email"
          autoComplete="username"
          placeholder="prenom.nom@usms.ac.ma"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label htmlFor="password">Mot de passe</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && (
          <p className="alert" role="alert">
            {error}
          </p>
        )}

        <button type="submit" disabled={busy || !email || !password}>
          {busy ? 'Connexion…' : 'Se connecter'}
        </button>
      </form>
    </main>
  )
}
