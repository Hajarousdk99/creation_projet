import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className="heroMessage">
      <h1>Page non trouvée</h1>
      <p className="muted">Cette page n’existe pas ou a été déplacée.</p>
      <Link to="/">Retour à l&apos;accueil</Link>
    </div>
  )
}
