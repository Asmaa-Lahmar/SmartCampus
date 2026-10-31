// Salles : la liste des salles du campus pour tous les utilisateurs (SC-21, EF-ROOM-01, ENF-10, ENF-18).

import { useEffect, useState } from 'react'
import { errorMessage } from '../api/client'
import { fetchRooms, ROOM_STATUS_LABELS, ROOM_TYPE_LABELS, ROOM_TYPES, type Room, type RoomType } from '../api/rooms'
import type { Session } from '../auth/session'
import { BuildingIcon, MapPinIcon, UsersIcon } from '../components/icons'
import { Link } from '../router'
import './RoomsPage.css'

interface Props {
  session: Session
}

export function RoomCard({ room }: { room: Room }) {
  return (
    <article className="room-card">
      <header className="room-card-head">
        <h3>{room.code}</h3>
        <span className={room.status === 'active' ? 'badge badge-success' : 'badge badge-warning'}>
          {ROOM_STATUS_LABELS[room.status]}
        </span>
      </header>
      <p className="room-type">{ROOM_TYPE_LABELS[room.room_type]}</p>
      <ul className="room-meta">
        <li>
          <MapPinIcon />
          {room.building}
        </li>
        <li>
          <UsersIcon />
          {room.capacity} places
        </li>
      </ul>
      {/* Le catalogue d'équipements arrive avec SC-31 (Sprint 3) */}
      <p className="room-equipment">Équipements : aucun renseigné</p>
      {room.description && <p className="room-description">{room.description}</p>}
    </article>
  )
}

export default function RoomsPage({ session }: Props) {
  const [rooms, setRooms] = useState<Room[] | null>(null)
  const [query, setQuery] = useState('')
  const [roomType, setRoomType] = useState<RoomType | ''>('')
  const [filters, setFilters] = useState({ q: '', room_type: '' as RoomType | '' })
  const [error, setError] = useState<string | null>(null)

  // La recherche par texte part 300 ms après la dernière frappe
  useEffect(() => {
    const timer = window.setTimeout(() => setFilters({ q: query.trim(), room_type: roomType }), 300)
    return () => window.clearTimeout(timer)
  }, [query, roomType])

  useEffect(() => {
    let active = true
    fetchRooms(session, filters)
      .then((list) => {
        if (!active) return
        setRooms(list)
        setError(null)
      })
      .catch((err) => active && setError(errorMessage(err)))
    return () => {
      active = false
    }
  }, [session, filters])

  const filtered = filters.q !== '' || filters.room_type !== ''

  return (
    <>
      <header className="page-head">
        <div>
          <h1>Salles</h1>
          <p>Bâtiment, type, capacité et statut de chaque salle du campus.</p>
        </div>
      </header>

      <div className="toolbar">
        <div className="toolbar-filters">
          <div className="field">
            <label htmlFor="rooms-search">Rechercher</label>
            <input
              id="rooms-search"
              className="input"
              type="search"
              placeholder="Code ou bâtiment"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="rooms-type">Type de salle</label>
            <select
              id="rooms-type"
              className="select"
              value={roomType}
              onChange={(event) => setRoomType(event.target.value as RoomType | '')}
            >
              <option value="">Tous les types</option>
              {ROOM_TYPES.map((type) => (
                <option key={type} value={type}>
                  {ROOM_TYPE_LABELS[type]}
                </option>
              ))}
            </select>
          </div>
        </div>
        {rooms && (
          <p className="toolbar-count" aria-live="polite">
            {rooms.length} salle{rooms.length > 1 ? 's' : ''}
          </p>
        )}
      </div>

      {error && (
        <p className="notice notice-error" role="alert">
          {error}
        </p>
      )}

      {rooms === null && !error && <p className="loading">Chargement des salles…</p>}

      {rooms !== null && rooms.length === 0 && (
        <div className="empty-state">
          <BuildingIcon className="empty-icon" />
          {filtered ? (
            <p>Aucune salle ne correspond à ces critères.</p>
          ) : (
            <>
              <p>Aucune salle n'est encore enregistrée.</p>
              {session.user.role === 'gestionnaire' && (
                <Link to="/gestion/salles" className="button-secondary">
                  Créer une salle
                </Link>
              )}
            </>
          )}
        </div>
      )}

      {rooms !== null && rooms.length > 0 && (
        <ul className="room-grid">
          {rooms.map((room) => (
            <li key={room.id}>
              <RoomCard room={room} />
            </li>
          ))}
        </ul>
      )}
    </>
  )
}
