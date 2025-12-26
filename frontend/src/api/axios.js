// minimal example (if not already)
import axios from 'axios'
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:5000/api' })
api.interceptors.request.use(cfg => {
  const t = localStorage.getItem('vpa_token')
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})
export default api
