// Accueil après connexion (SC-11). SC-15 ajoute la déconnexion.

import { ROLE_LABELS, type Session } from '../auth/session'

interface Props {
  session: Session
  onLoggedOut: () => void
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

export default function HomePage({ session }: Props) {
  const { user } = session

  return (
    <div className="page">
      <header className="topbar">
        <span className="brand">
          <img src="/favicon.svg" alt="" width={28} height={28} />
          SmartCampus
        </span>
        <span className="topbar-user">{user.full_name}</span>
      </header>

      <main className="home">
        <h1>Bonjour {user.full_name}</h1>
        <p className="subtitle">
          {ROLE_LABELS[user.role]} · {user.email}
        </p>

        <section className="card">
          <h2>Votre session</h2>
          <p>
            Vous êtes connecté jusqu'à <strong>{formatTime(session.expiresAt)}</strong>. Au-delà, la
            connexion vous sera redemandée.
          </p>
        </section>

        <section className="card card-muted">
          <h2>Bientôt dans SmartCampus</h2>
          <ul>
            <li>Rechercher une salle libre (Sprint 2)</li>
            <li>Réserver et annuler une salle (Sprint 3)</li>
            <li>Déposer et suivre une demande administrative (Sprint 4)</li>
          </ul>
        </section>
      </main>
    </div>
  )
}
