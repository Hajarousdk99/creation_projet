import './App.css'
import { Link, Route, Routes, useNavigate } from 'react-router-dom'

import { clearTokens, getAccessToken } from './auth'
import CartPage from './pages/CartPage.jsx'
import CheckoutCancelPage from './pages/CheckoutCancelPage.jsx'
import CheckoutSuccessPage from './pages/CheckoutSuccessPage.jsx'
import CategoryPage from './pages/CategoryPage.jsx'
import HomePage from './pages/HomePage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import ProductDetailPage from './pages/ProductDetailPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'

function App() {
  const navigate = useNavigate()
  const isAuthed = Boolean(getAccessToken())

  return (
    <div className="appShell">
      <header className="topNav">
        <Link className="brand" to="/">
          Boutique Djellaba
        </Link>
        <nav className="navLinks">
          <Link to="/">Accueil</Link>
          <Link to="/cart">Panier</Link>
          {!isAuthed ? (
            <>
              <Link to="/login">Connexion</Link>
              <Link to="/register">Créer un compte</Link>
            </>
          ) : (
            <button
              className="linkButton"
              onClick={() => {
                clearTokens()
                navigate('/login')
              }}
            >
              Déconnexion
            </button>
          )}
        </nav>
      </header>

      <main className="container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/categorie/:slug" element={<CategoryPage />} />
          <Route path="/categorie/:slug/:subSlug" element={<CategoryPage />} />
          <Route path="/products/:id" element={<ProductDetailPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout/success" element={<CheckoutSuccessPage />} />
          <Route path="/checkout/cancel" element={<CheckoutCancelPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
