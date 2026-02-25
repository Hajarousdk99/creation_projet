import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { api } from '../api/client'
import { getAccessToken } from '../auth'

const STATUS_LABELS = {
  pending: 'En attente',
  paid: 'Payée',
  cancelled: 'Annulée',
}

function formatDate(iso) {
  if (!iso) return '–'
  const d = new Date(iso)
  return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

export default function OrdersPage() {
  const isAuthed = Boolean(getAccessToken())
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!isAuthed) {
      setLoading(false)
      return
    }
    setLoading(true)
    setError('')
    api('/api/orders/', { auth: true })
      .then((data) => setOrders(Array.isArray(data) ? data : []))
      .catch((e) => setError(e?.message || 'Erreur'))
      .finally(() => setLoading(false))
  }, [isAuthed])

  if (!isAuthed) {
    return (
      <div className="stack small">
        <h1>Mes commandes</h1>
        <div className="card">
          <p>Tu dois être connecté pour voir tes commandes.</p>
          <Link to="/login">Se connecter</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="stack">
      <h1>Mes commandes</h1>
      {loading && <div className="card">Chargement…</div>}
      {error && <div className="card error">Erreur : {error}</div>}
      {!loading && !error && orders.length === 0 && (
        <div className="card">
          <p>Aucune commande pour le moment.</p>
          <Link to="/">Voir la boutique</Link>
        </div>
      )}
      {!loading && !error && orders.length > 0 && (
        <div className="stack small">
          {orders.map((order) => (
            <div key={order.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                <strong>Commande #{order.id}</strong>
                <span className="muted">{formatDate(order.created_at)}</span>
              </div>
              <p style={{ margin: '0.5rem 0 0 0' }}>
                Statut : <strong>{STATUS_LABELS[order.status] ?? order.status_display ?? order.status}</strong>
                {' · '}
                Total : {Number(order.total_amount).toFixed(2)} {order.currency?.toUpperCase()}
              </p>
              {order.items?.length > 0 && (
                <ul style={{ marginTop: '0.75rem', paddingLeft: '1.25rem' }}>
                  {order.items.map((item) => (
                    <li key={item.id}>
                      {item.product_name} × {item.quantity} — {Number(item.line_total).toFixed(2)} €
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
