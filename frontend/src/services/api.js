import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Persons API
export const personAPI = {
  getAll: (params = {}) => apiClient.get('/persons/', { params }),
  getById: (id) => apiClient.get(`/persons/${id}/`),
  create: (data) => apiClient.post('/persons/', data),
  update: (id, data) => apiClient.put(`/persons/${id}/`, data),
  delete: (id) => apiClient.delete(`/persons/${id}/`),
  importCSV: (records) => apiClient.post('/persons/bulk_import/', { records })
}

// WebForm Submissions API
export const webformAPI = {
  getAll: (params = {}) => apiClient.get('/webforms/', { params }),
  getById: (id) => apiClient.get(`/webforms/${id}/`),
  getByPerson: (personId) => apiClient.get('/webforms/', { params: { person: personId } }),
  create: (data) => apiClient.post('/webforms/', data),
  update: (id, data) => apiClient.put(`/webforms/${id}/`, data),
  delete: (id) => apiClient.delete(`/webforms/${id}/`),
  getAllSubmissions: (params = {}) => apiClient.get('/webform-submissions/', { params })
}

// Dashboard API
export const dashboardAPI = {
  getStats: () => apiClient.get('/stats/')
}

export default apiClient
