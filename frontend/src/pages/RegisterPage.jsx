import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { api } from '../api/client'
import { setTokens } from '../auth'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function onSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await api('/api/auth/register/', {
        method: 'POST',
        body: { username, email, password },
      })
      const data = await api('/api/auth/token/', {
        method: 'POST',
        body: { username, password },
      })
      setTokens({ access: data.access, refresh: data.refresh })
      navigate('/')
    } catch (err) {
      const msg = err?.data ? JSON.stringify(err.data) : err.message
      setError(msg || 'Erreur')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="stack small">
      <h1>Créer un compte</h1>
      <form className="card form" onSubmit={onSubmit}>
        <label>
          Nom d’utilisateur
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
        </label>
        <label>
          Email (optionnel)
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" autoComplete="email" />
        </label>
        <label>
          Mot de passe
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" autoComplete="new-password" />
        </label>
        {error && <div className="errorText">{error}</div>}
        <button disabled={loading || !username || password.length < 8} type="submit">
          {loading ? 'Création…' : 'Créer le compte'}
        </button>
      </form>

      <div className="muted">
        Déjà un compte ? <Link to="/login">Se connecter</Link>
      </div>
    </div>
  )
}

