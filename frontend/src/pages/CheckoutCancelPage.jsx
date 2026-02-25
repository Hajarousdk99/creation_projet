import { Link } from 'react-router-dom'

export default function CheckoutCancelPage() {
  return (
    <div className="heroMessage">
      <h1>Paiement annulé</h1>
      <div className="card">Vous pouvez réessayer depuis le panier quand vous voulez.</div>
      <Link to="/cart">Retour au panier</Link>
    </div>
  )
}

