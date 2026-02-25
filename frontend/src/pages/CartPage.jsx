import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { api } from '../api/client'
import { getAccessToken } from '../auth'

function calcTotal(items) {
  return items.reduce((acc, it) => acc + Number(it.product?.price || 0) * Number(it.quantity || 0), 0)
}

export default function CartPage() {
  const navigate = useNavigate()
  const isAuthed = Boolean(getAccessToken())
  const [cart, setCart] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const refresh = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const data = await api('/api/cart/', { auth: true })
      setCart(data)
    } catch (e) {
      setError(e.message || 'Erreur')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (!isAuthed) return
    refresh()
  }, [isAuthed, refresh])

  async function removeItem(id) {
    await api(`/api/cart/items/${id}/`, { method: 'DELETE', auth: true })
    refresh()
  }

  async function updateQty(id, quantity) {
    await api(`/api/cart/items/${id}/`, { method: 'PATCH', auth: true, body: { quantity } })
    refresh()
  }

  async function checkout() {
    try {
      const data = await api('/api/payments/create-checkout-session/', { method: 'POST', auth: true })
      window.location.href = data.checkout_url
    } catch (e) {
      alert(e.message || 'Erreur')
    }
  }

  if (!isAuthed) {
    return (
      <div className="card">
        Tu dois être connecté. <Link to="/login">Aller à la connexion</Link>
      </div>
    )
  }

  if (loading) return <div className="card">Chargement…</div>
  if (error) return <div className="card error">Erreur: {error}</div>

  const items = cart?.items || []
  const total = calcTotal(items)

  return (
    <div className="stack">
      <div className="row spread">
        <h1>Panier</h1>
        <button className="secondary" onClick={() => navigate('/')}>
          Continuer mes achats
        </button>
      </div>

      {items.length === 0 ? (
        <div className="card">Panier vide.</div>
      ) : (
        <div className="stack">
          {items.map((it) => (
            <div key={it.id} className="card row spread">
              <div className="stack tight">
                <div className="productTitle">{it.product?.name}</div>
                <div className="muted">
                  {it.product?.price} {String(it.product?.currency || '').toUpperCase()}
                </div>
              </div>
              <div className="row">
                <input
                  className="qty"
                  type="number"
                  min="1"
                  value={it.quantity}
                  onChange={(e) => updateQty(it.id, Number(e.target.value))}
                />
                <button className="danger" onClick={() => removeItem(it.id)}>
                  Retirer
                </button>
              </div>
            </div>
          ))}

          <div className="card cartSummary row spread">
            <div className="stack tight">
              <div className="muted">Total estimé</div>
              <div className="price">{total.toFixed(2)} EUR</div>
            </div>
            <button className="checkoutBtn" onClick={checkout}>Payer avec Stripe</button>
          </div>
        </div>
      )}
    </div>
  )
}

