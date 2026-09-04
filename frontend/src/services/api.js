import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function fetchMetrics() {
  const { data } = await api.get('/metrics')
  return data
}

export async function fetchExceptions() {
  const { data } = await api.get('/exceptions')
  return data
}

export async function investigateException(orderId) {
  const { data } = await api.post(`/exceptions/${encodeURIComponent(orderId)}/investigate`)
  return data
}

export async function resolveException(orderId, decision, reason) {
  const { data } = await api.post(`/exceptions/${encodeURIComponent(orderId)}/resolve`, {
    decision,
    reason,
  })
  return data
}

export async function fetchAudit(orderId) {
  const { data } = await api.get(`/exceptions/${encodeURIComponent(orderId)}/audit`)
  return data
}
