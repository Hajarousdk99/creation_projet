import { getAccessToken } from '../auth'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function api(path, { method = 'GET', body, auth = false } = {}) {
  const headers = { Accept: 'application/json' }
  if (body !== undefined) headers['Content-Type'] = 'application/json'

  if (auth) {
    const token = getAccessToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  let res
  try {
    res = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch (e) {
    if (e?.message === 'Failed to fetch' || e?.name === 'TypeError') {
      throw new Error(
        'Impossible de joindre le serveur. Vérifiez que le backend Django tourne (python manage.py runserver sur le port 8000).'
      )
    }
    throw e
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

