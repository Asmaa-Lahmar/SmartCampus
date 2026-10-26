// Accueil de SmartCampus (SC-11, SC-15) : même système de design que la page de connexion.

import { useEffect, useState, type ComponentType } from 'react'
import { fetchMe, logout, setUnauthorizedHandler } from '../api/client'
import { clearSession, isExpired, ROLE_LABELS, type Session } from '../auth/session'
import {
  BuildingIcon,
  CalendarCheckIcon,
  CalendarIcon,
  FileIcon,
  GridIcon,
  HomeIcon,
  LogoutIcon,
  MailIcon,
  SearchIcon,
  UserIcon,
  type IconProps,
} from '../components/icons'

interface Props {
  session: Session
  onLoggedOut: () => void
}

interface Service {
  title: string

  description: string
  Icon: ComponentType<IconProps>
}

// Services à venir, dans l'ordre du planning des sprints (cahier des charges, chapitre 8)
const SERVICES: Service[] = [
  {
    title: 'Recherche de salle',
    
    description: "Consultez la disponibilité des salles et trouvez l'espace adapté à vos besoins.",
    Icon: SearchIcon,
  },
  {
    title: 'Réservation de salle',
  
    description: 'Réservez une salle en quelques clics pour vos cours, réunions ou événements.',
    Icon: CalendarCheckIcon,
  },
  {
    title: 'Démarches administratives',
    
    description: "Effectuez vos demandes administratives en ligne et suivez leur état d'avancement.",
    Icon: FileIcon,
  },
]

function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

function formatToday(): string {
  const label = new Date().toLocaleDateString('fr-FR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
  return label.charAt(0).toUpperCase() + label.slice(1)
}

function nameParts(fullName: string): string[] {
  return fullName.trim().split(/\s+/).filter(Boolean)
}

function initials(fullName: string): string {
  return nameParts(fullName)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join('')
}

export default function HomePage({ session, onLoggedOut }: Props) {
  const [user, setUser] = useState(session.user)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    setUnauthorizedHandler(onLoggedOut)

    const checkExpiry = () => {
      if (isExpired(session)) {
        clearSession()
        onLoggedOut()
      }
    }
    window.addEventListener('focus', checkExpiry)
    document.addEventListener('visibilitychange', checkExpiry)

    fetchMe(session)
      .then(setUser)
      .catch(() => {
        // Profil non rafraîchi : celui de la session reste affiché
      })

    return () => {
      setUnauthorizedHandler(null)
      window.removeEventListener('focus', checkExpiry)
      document.removeEventListener('visibilitychange', checkExpiry)
    }
  }, [session, onLoggedOut])

  async function handleLogout() {
    setBusy(true)
    try {
      await logout(session)
    } catch {
      // Même si l'API est injoignable, la session locale est effacée (voir logout)
    } finally {
      onLoggedOut()
    }
  }

  const firstName = nameParts(user.full_name)[0] ?? user.full_name
  const roleLabel = ROLE_LABELS[user.role]

  return (
    <div className="home-page">
      <header className="topbar">
        <div className="topbar-inner home-container">
          <div className="topbar-brand">
            <span className="wordmark">
              Smart<span>Campus</span>
            </span>
          
          </div>

          <nav className="topnav" aria-label="Navigation principale">
            <a className="topnav-link is-active" href="#" aria-current="page">
              <HomeIcon />
              Accueil
            </a>
            <a className="topnav-link" href="#services">
              <GridIcon />
              Services campus
            </a>
            <span className="topnav-link is-soon" aria-disabled="true" title="Disponible au Sprint 4">
              <FileIcon />
              Mes demandes
              <span className="visually-hidden"> (disponible au Sprint 4)</span>
            </span>
          </nav>

          <div className="topbar-user">
            <span className="avatar" aria-hidden="true">
              {initials(user.full_name)}
            </span>
            <span className="topbar-user-text">
              <strong>{user.full_name}</strong>
              <span>{roleLabel}</span>
            </span>
          </div>

          <button type="button" className="button-secondary logout" onClick={handleLogout} disabled={busy}>
            <LogoutIcon />
            <span className="logout-label">{busy ? 'Déconnexion…' : 'Se déconnecter'}</span>
          </button>
        </div>
      </header>

      <main className="home home-container">
        <section className="home-greeting">
          <div>
            <div className="home-title-row">
              <h1>Bonjour, {firstName} </h1>
             
            </div>
            <p className="home-subtitle">Bon retour sur SmartCampus </p>
          </div>

          <div className="home-meta">
            <p className="home-meta-date">
              <CalendarIcon />
              {formatToday()}
            </p>
           
          </div>
        </section>

        <section className="home-hero" aria-labelledby="hero-title">
          <div className="home-hero-text">
            <h2 id="hero-title">Tout votre campus, au même endroit.</h2>
            <p>Réservez vos espaces, effectuez vos démarches et suivez vos demandes en toute simplicité.</p>
            <span className="home-hero-rule" aria-hidden="true" />
          </div>
          <div className="home-hero-art" aria-hidden="true">
            <img src="/login-illustration.svg" alt="" />
          </div>
        </section>

        <section id="services" className="home-section" aria-labelledby="services-title">
          <h2 id="services-title" className="home-section-title">
            Services campus
          </h2>
          <ul className="service-grid">
            {SERVICES.map(({ title, description, Icon }) => (
              <li key={title} className="service-card">
                <span className="service-icon">
                  <Icon />
                </span>
                <div>
                  <h3>{title}</h3>
                  
                  <p>{description}</p>
                </div>
              </li>
            ))}
          </ul>
        </section>

        <section className="home-section" aria-labelledby="account-title">
          <h2 id="account-title" className="home-section-title">
            Votre compte
          </h2>
          <div className="account-card">
            <div className="account-person">
              <span className="account-avatar">
                <UserIcon />
              </span>
              <div>
                <strong>{user.full_name}</strong>
                <span>{roleLabel}</span>
              </div>
            </div>
            <dl className="account-details">
              <div className="account-item">
                <dt>
                  <MailIcon />
                  E-mail institutionnel
                </dt>
                <dd>{user.email}</dd>
              </div>
              <div className="account-item">
                <dt>
                  <BuildingIcon />
                  Établissement
                </dt>
                <dd>ENSA Khouribga</dd>
              </div>
            </dl>
          </div>
        </section>
      </main>
    </div>
  )
}
