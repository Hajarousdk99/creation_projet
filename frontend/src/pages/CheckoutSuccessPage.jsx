import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api } from '../api/client'

export default function CheckoutSuccessPage() {
  const [searchParams] = useSearchParams()
  const [confirmed, setConfirmed] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const sessionId = searchParams.get('session_id')
    if (!sessionId) {
      setError('Paramètre session_id manquant.')
      return
    }
    api(`/api/payments/confirm-checkout-session/?session_id=${encodeURIComponent(sessionId)}`, { auth: true })
      .then(() => setConfirmed(true))
      .catch((err) => setError(err?.message || 'Impossible de confirmer la commande.'))
  }, [searchParams])

  return (
    <div className="heroMessage">
      <h1>Paiement réussi</h1>
      <div className="card">
        {error && <p className="error">{error}</p>}
        {!error && !confirmed && <p>Confirmation de votre commande en cours…</p>}
        {!error && confirmed && <p>Merci pour votre achat. Votre commande est bien enregistrée.</p>}
      </div>
      <Link to="/">Retour à l&apos;accueil</Link>
    </div>
  )
} 

