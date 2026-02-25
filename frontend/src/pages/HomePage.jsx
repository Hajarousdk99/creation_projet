import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { getAccessToken } from '../auth'
import { api } from '../api/client'

export default function HomePage() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const isAuthed = Boolean(getAccessToken())

  useEffect(() => {
    let cancelled = false
    api('/api/categories/')
      .then((data) => {
        if (cancelled) return
        setCategories(Array.isArray(data) ? data : [])
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
  }, [])

  return (
    <div className="stack">
      <div className="pageHeader">
        <h1>Boutique</h1>
        <p className="tagline">L'art d'être soi, pleinement féminin</p>
        <p className="muted">
          {isAuthed ? (
            <>
              Passe au <Link to="/cart">panier</Link> pour finaliser ta commande.
            </>
          ) : (
            <>Connecte-toi pour ajouter au panier et payer.</>
          )}
        </p>
      </div>

      {loading && <div className="card">Chargement…</div>}
      {error && <div className="card error">Erreur: {error}</div>}

      {!loading && !error && (
        <div className="categoryChoiceGrid">
          {categories.map((cat) => (
            <Link to={`/categorie/${cat.slug}`} className="card categoryChoiceCard" key={cat.id}>
              <span className="categoryChoiceTitle">{cat.name}</span>
              <span className="categoryChoiceSub">Voir les produits →</span>
            </Link>
          ))}
        </div>
      )}

      {!loading && !error && categories.length === 0 && (
        <div className="card">Aucune catégorie pour l'instant.</div>
      )}
    </div>
  )
}
