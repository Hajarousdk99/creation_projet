import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { api } from '../api/client'
import { setTokens } from '../auth'

export default function LoginPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function onSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const data = await api('/api/auth/token/', {
        method: 'POST',
        body: { username, password },
      })
      setTokens({ access: data.access, refresh: data.refresh })
      navigate('/')
    } catch (err) {
      setError(err.message || 'Erreur')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="stack small">
      <h1>Connexion</h1>
      <form className="card form" onSubmit={onSubmit}>
        <label>
          Nom d’utilisateur
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
        </label>
        <label>
          Mot de passe
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            autoComplete="current-password"
          />
        </label>
        {error && <div className="errorText">{error}</div>}
        <button disabled={loading || !username || !password} type="submit">
          {loading ? 'Connexion…' : 'Se connecter'}
        </button>
      </form>

      <div className="muted">
        Pas de compte ? <Link to="/register">Créer un compte</Link>
      </div>
    </div>
  )
}

