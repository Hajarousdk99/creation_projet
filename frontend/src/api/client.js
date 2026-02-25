import { getAccessToken, getRefreshToken, setTokens, clearTokens } from '../auth'

const envUrl = import.meta.env.VITE_API_BASE_URL || ''
const isBrowserLocal =
  typeof window !== 'undefined' &&
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
const hasProdEnv = envUrl && !envUrl.includes('localhost') && !envUrl.includes('127.0.0.1')

export const API_BASE_URL = hasProdEnv
  ? envUrl
  : isBrowserLocal
    ? (envUrl || 'http://localhost:8000')
    : 'https://creation-projet.onrender.com'

async function doFetch(path, options) {
  const { method = 'GET', body, headers: extraHeaders } = options
  const headers = { Accept: 'application/json', ...extraHeaders }
  if (body !== undefined) headers['Content-Type'] = 'application/json'

  const res = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  return res
}

export async function api(path, { method = 'GET', body, auth = false, _retrying = false } = {}) {
  const headers = {}
  if (auth) {
    const token = getAccessToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  let res
  try {
    res = await doFetch(path, { method, body, headers })
  } catch (e) {
    if (e?.message === 'Failed to fetch' || e?.name === 'TypeError') {
      const isLocal = API_BASE_URL.includes('localhost') || API_BASE_URL.includes('127.0.0.1')
      const isProd = !isLocal
      const message = isProd
        ? 'Le serveur ne répond pas. Sur l\'offre gratuite il peut mettre 30–60 secondes à démarrer. Réessayez dans un instant.'
        : 'Impossible de joindre le serveur. Vérifiez que le backend Django tourne (python manage.py runserver sur le port 8000).'
      throw new Error(message)
    }
    throw e
  }

  if (res.status === 401 && auth && !_retrying) {
    const refreshToken = getRefreshToken()
    if (refreshToken) {
      try {
        const refreshRes = await doFetch('/api/auth/token/refresh/', {
          method: 'POST',
          body: { refresh: refreshToken },
        })
        if (refreshRes.ok) {
          const data = await refreshRes.json()
          if (data.access) {
            setTokens({ access: data.access, refresh: data.refresh ?? refreshToken })
            return api(path, { method, body, auth, _retrying: true })
          }
        }
      } catch (_) {
        // refresh failed
      }
      clearTokens()
    }
  }

  const contentType = res.headers.get('content-type') || ''
  const isJson = contentType.includes('application/json')
  const data = isJson ? await res.json() : null

  if (!res.ok) {
    const detail = data?.detail || `HTTP ${res.status}`
    const err = new Error(detail)
    err.status = res.status
    err.data = data
    throw err
  }

  return data
}

