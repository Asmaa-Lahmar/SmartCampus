// Session de l'utilisateur connecté (SC-11).
// sessionStorage : la session disparaît à la fermeture de l'onglet (poste partagé).

export type Role = 'etudiant' | 'enseignant' | 'gestionnaire' | 'scolarite' | 'administrateur'

export interface SessionUser {
  id: number
  email: string
  full_name: string
  role: Role
}

export interface Session {
  accessToken: string
  expiresAt: string // date ISO renvoyée par l'API
  user: SessionUser
}

export const ROLE_LABELS: Record<Role, string> = {
  etudiant: 'Étudiant',
  enseignant: 'Enseignant',
  gestionnaire: 'Gestionnaire des salles',
  scolarite: 'Agent de scolarité',
  administrateur: 'Administrateur système',
}

const STORAGE_KEY = 'smartcampus.session'

export function isExpired(session: Session): boolean {
  return new Date(session.expiresAt).getTime() <= Date.now()
}

export function loadSession(): Session | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const session = JSON.parse(raw) as Session
    if (isExpired(session)) {
      clearSession()
      return null
    }
    return session
  } catch {
    return null
  }
}

export function saveSession(session: Session): void {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(session))
  } catch {
    // Stockage indisponible (navigation privée) : la session reste en mémoire
  }
}

export function clearSession(): void {
  try {
    sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    // rien à effacer
  }
}
