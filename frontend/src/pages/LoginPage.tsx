// Connexion à SmartCampus (SC-11, EF-AUTH-01, EF-AUTH-03) : page plein écran, d'après la maquette validée.

import { useState, type FormEvent } from 'react'
import { ApiError, login } from '../api/client'
import { saveSession, type Session } from '../auth/session'
import { ArrowIcon, CheckIcon, EyeIcon, EyeOffIcon, LockIcon, MailIcon } from '../components/icons'

const INVALID_CREDENTIALS = 'E-mail ou mot de passe incorrect'
const SERVER_UNREACHABLE = 'Serveur injoignable. Réessayez dans un instant.'

const PERKS = ['Rapide et sécurisé', 'Accessible partout', 'Conçu pour la communauté ENSA']

interface Props {
  onLoggedIn: (session: Session) => void
}

export default function LoginPage({ onLoggedIn }: Props) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
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
        // Message générique : ne jamais dire lequel des deux champs est faux (EF-AUTH-03)
        setError(err.status === 401 || !err.detail ? INVALID_CREDENTIALS : err.detail)
      } else {
        setError(SERVER_UNREACHABLE)
      }
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="login-page">
      <img className="login-illustration" src="/login-illustration.svg" alt="" />

      <section className="login-hero">
        <div className="login-brand">
          <span className="login-wordmark">
            Smart<span>Campus</span>
          </span>
         
        </div>

        <h1>Simplifiez votre vie universitaire.</h1>
        <p className="login-lead">
          Réservation de salles, demandes administratives et bien plus encore.
        </p>

        <ul className="login-perks">
          {PERKS.map((perk) => (
            <li key={perk}>
              <CheckIcon className="login-check" />
              {perk}
            </li>
          ))}
        </ul>
      </section>

      <form className="login-card" onSubmit={handleSubmit} noValidate>
        <div className="login-card-icon">
          <LockIcon />
        </div>
        <h2>Connexion</h2>
        <p className="login-card-subtitle">Connectez-vous à votre compte</p>

        <label htmlFor="email">E-mail institutionnel</label>
        <div className="login-field">
          <MailIcon className="login-field-icon" />
          <input
            id="email"
            type="email"
            autoComplete="username"
            placeholder="prenom.nom@usms.ac.ma"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <label htmlFor="password">Mot de passe</label>
        <div className="login-field login-field-password">
          <LockIcon className="login-field-icon" />
          <input
            id="password"
            type={showPassword ? 'text' : 'password'}
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button
            type="button"
            className="login-eye"
            onClick={() => setShowPassword((shown) => !shown)}
            aria-label={showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'}
            aria-pressed={showPassword}
          >
            {showPassword ? <EyeOffIcon /> : <EyeIcon />}
          </button>
        </div>

        {error && (
          <p className="alert" role="alert">
            {error}
          </p>
        )}

        <button type="submit" className="login-submit" disabled={busy || !email || !password}>
          {busy ? 'Connexion…' : 'Se connecter'}
          <ArrowIcon className="login-submit-arrow" />
        </button>
      </form>
    </main>
  )
}
