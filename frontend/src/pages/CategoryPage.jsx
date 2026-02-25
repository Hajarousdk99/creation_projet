import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { getAccessToken } from '../auth'
import { api } from '../api/client'

export default function CategoryPage() {
  const { slug, subSlug } = useParams()
  const [subcategories, setSubcategories] = useState([])
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const isAuthed = Boolean(getAccessToken())

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError('')

    const parentSlug = subSlug || slug
    const categorySlug = subSlug || null

    api(`/api/categories/?parent=${encodeURIComponent(parentSlug)}`)
      .then((cats) => {
        if (cancelled) return
        const list = Array.isArray(cats) ? cats : []
        setSubcategories(list)
        const hasChildren = list.length > 0
        const productsUrl = categorySlug && !hasChildren
          ? `/api/products/?category=${encodeURIComponent(categorySlug)}`
          : `/api/products/?parent=${encodeURIComponent(parentSlug)}`
        return api(productsUrl)
      })
      .then((prods) => {
        if (cancelled) return
        setProducts(Array.isArray(prods) ? prods : [])
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
  }, [slug, subSlug])

  async function addToCart(productId) {
    try {
      await api('/api/cart/items/', {
        method: 'POST',
        auth: true,
        body: { product_id: productId, quantity: 1 },
      })
      alert('Ajouté au panier')
    } catch (e) {
      alert(e.message || 'Erreur')
    }
  }

  const title = subSlug
    ? (subcategories.find((c) => c.slug === subSlug)?.name ||
        (subSlug === 'robes-traditionnelles' ? 'Robes' : subSlug === 'robe-simple' ? 'Robe simple' : subSlug === 'abaya' ? 'Abaya' : subSlug))
    : slug === 'femme'
      ? 'Femme'
      : slug === 'homme'
        ? 'Homme'
        : slug

  return (
    <div className="stack">
      <Link to={subSlug && slug ? `/categorie/${slug}` : '/'} className="backLink">
        ← Retour à {subSlug && slug ? (slug === 'femme' ? 'Femme' : slug === 'homme' ? 'Homme' : 'l\'accueil') : 'l\'accueil'}
      </Link>
      <h1 className="categoryPageTitle">{title}</h1>

      {subcategories.length > 0 && (
        <div className="subcategorySection">
          <h2 className="subcategorySectionTitle">Catégories</h2>
          <div className="subcategoryGrid">
            {subcategories.map((sub) => (
              <Link
                to={`/categorie/${slug}/${sub.slug}`}
                className={`card subcategoryCard ${subSlug === sub.slug ? 'subcategoryCardActive' : ''}`}
                key={sub.id}
              >
                <span className="subcategoryName">{sub.name}</span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {loading && <div className="card">Chargement…</div>}
      {error && <div className="card error">Erreur: {error}</div>}

      {!loading && !error && (
        <>
          <h2 className="productsSectionTitle">Produits</h2>
          {products.length === 0 ? (
            <div className="card">Aucun produit dans cette catégorie.</div>
          ) : (
            <div className="grid">
              {products.map((p) => (
                <div className="card productCard" key={p.id}>
                  <Link to={`/products/${p.id}`} className="productCardImageWrap">
                    {p.image_url ? (
                      <img src={p.image_url} alt={p.name} className="productCardImage" />
                    ) : (
                      <div className="productCardImagePlaceholder" aria-hidden>Robe</div>
                    )}
                  </Link>
                  <Link to={`/products/${p.id}`} className="productTitle productCardTitleLink">
                    {p.name}
                  </Link>
                  <div className="muted">{p.description || '—'}</div>
                  <div className="price">
                    {p.price} {String(p.currency || '').toUpperCase()}
                  </div>
                  <div className="row">
                    <button disabled={!isAuthed} onClick={() => addToCart(p.id)}>
                      Ajouter au panier
                    </button>
                    {!isAuthed && (
                      <Link className="secondary" to="/login">
                        Se connecter
                      </Link>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}
