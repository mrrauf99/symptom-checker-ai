import apiClient from './client.js'

export const sessionsAPI = {
  createSession: async (title) => {
    const res = await apiClient.post('/sessions', { title })
    return res.data
  },

  getSessions: async () => {
    const res = await apiClient.get('/sessions')
    return res.data
  },

  getSession: async (sessionId) => {
    const res = await apiClient.get(`/sessions/${sessionId}`)
    return res.data
  },

  endSession: async (sessionId) => {
    const res = await apiClient.patch(`/sessions/${sessionId}/end`)
    return res.data
  },

  deleteSession: async (sessionId) => {
    const res = await apiClient.delete(`/sessions/${sessionId}`)
    return res.data
  },
}
