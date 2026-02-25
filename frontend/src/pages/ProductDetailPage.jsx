import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { getAccessToken } from '../auth'
import { api } from '../api/client'

export default function ProductDetailPage() {
  const { id } = useParams()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const isAuthed = Boolean(getAccessToken())

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError('')
    api(`/api/products/${id}/`)
      .then((data) => {
        if (cancelled) return
        setProduct(data)
      })
      .catch((e) => {
        if (cancelled) return
        setError(e.message || 'Erreur')
      })
      .finally(() => {
        if (cancelled) return
        setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [id])

  async function addToCart() {
    try {
      await api('/api/cart/items/', {
        method: 'POST',
        auth: true,
        body: { product_id: product.id, quantity: 1 },
      })
      alert('Ajouté au panier')
    } catch (e) {
      alert(e.message || 'Erreur')
    }
  }

  if (loading) return <div className="card">Chargement…</div>
  if (error) {
    return (
      <div className="stack">
        <div className="card error">Erreur: {error}</div>
        <Link to="/">Retour aux djellabas</Link>
      </div>
    )
  }
  if (!product) return null

  return (
    <div className="stack productDetailPage">
      <Link to="/" className="backLink">
        ← Retour aux djellabas
      </Link>
      <div className="productDetailCard">
        <div className="productDetailImageWrap">
          {product.image_url ? (
            <img src={product.image_url} alt={product.name} className="productDetailImage" />
          ) : (
            <div className="productDetailImagePlaceholder">Robe</div>
          )}
        </div>
        <div className="productDetailContent">
          <h1 className="productDetailTitle">{product.name}</h1>
          <p className="productDetailDescription">{product.description || '—'}</p>
          <div className="productDetailPrice">
            {product.price} {String(product.currency || '').toUpperCase()}
          </div>
          <div className="productDetailActions">
            {isAuthed ? (
              <button onClick={addToCart}>Ajouter au panier</button>
            ) : (
              <Link className="secondary" to="/login">
                Se connecter pour ajouter au panier
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
