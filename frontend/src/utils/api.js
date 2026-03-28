export const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Normalize image URLs: Cloudinary/external URLs pass through as-is; relative paths get BASE_URL prepended
export function resolveImageUrl(url) {
  if (!url) return url
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  return url.startsWith('/') ? `${BASE_URL}${url}` : url
}

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw { status: res.status, detail: err.detail || 'Request failed' }
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  get:    (path)         => request(path),
  post:   (path, body)   => request(path, { method: 'POST', body: JSON.stringify(body) }),
  put:    (path, body)   => request(path, { method: 'PUT',   body: JSON.stringify(body) }),
  patch:  (path, body)   => request(path, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: (path)         => request(path, { method: 'DELETE' }),
}
