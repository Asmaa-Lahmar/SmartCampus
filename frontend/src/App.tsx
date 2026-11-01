// Choisit la page à afficher selon la session, le rôle et l'adresse (SC-11, SC-17, SC-20 à SC-23).

import { useCallback, useState } from 'react'
import { loadSession, saveSession, type Session, type SessionUser } from './auth/session'
import AppLayout from './components/AppLayout'
import AccountsPage from './pages/AccountsPage'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import ManageRoomsPage from './pages/ManageRoomsPage'
import RoomPlanningPage from './pages/RoomPlanningPage'
import RoomsPage from './pages/RoomsPage'
import StatusPage from './pages/StatusPage'
import { matchPath, useLocation, type Location } from './router'

function Forbidden() {
  return <StatusPage title="Accès refusé" message="Votre rôle ne permet pas d'ouvrir cette page." />
}

function renderPage(session: Session, location: Location) {
  const { path } = location
  if (path === '/') return <HomePage user={session.user} />
  if (path === '/salles') return <RoomsPage session={session} location={location} />
  const room = matchPath('/salles/:id', path)
  if (room && /^\d+$/.test(room.id)) {
    return <RoomPlanningPage key={room.id} session={session} roomId={Number(room.id)} location={location} />
  }
  if (path === '/gestion/salles') {
    if (session.user.role !== 'gestionnaire') return <Forbidden />
    return <ManageRoomsPage session={session} />
  }
  if (path === '/admin/comptes') {
    // L'API refuse aussi (403) : ce contrôle évite seulement d'afficher une page inutilisable
    if (session.user.role !== 'administrateur') return <Forbidden />
    return <AccountsPage session={session} />
  }
  return <StatusPage title="Page introuvable" message="Cette adresse ne correspond à aucune page de SmartCampus." />
}

export default function App() {
  const [session, setSession] = useState<Session | null>(() => loadSession())
  const location = useLocation()

  const handleLoggedOut = useCallback(() => setSession(null), [])

  // Nom ou rôle modifié (rafraîchi par l'API) : la session enregistrée suit
  const handleUserUpdated = useCallback((user: SessionUser) => {
    setSession((current) => {
      if (!current || JSON.stringify(current.user) === JSON.stringify(user)) return current
      const next = { ...current, user }
      saveSession(next)
      return next
    })
  }, [])

  if (!session) return <LoginPage onLoggedIn={setSession} />

  return (
    <AppLayout
      session={session}
      path={location.path}
      onLoggedOut={handleLoggedOut}
      onUserUpdated={handleUserUpdated}
    >
      {renderPage(session, location)}
    </AppLayout>
  )
}
