import apiClient from './client.js'

export const messagesAPI = {
  saveMessage: async (data) => {
    const res = await apiClient.post('/messages', data)
    return res.data
  },

  getSessionMessages: async (sessionId) => {
    const res = await apiClient.get(`/messages/${sessionId}`)
    return res.data
  },
}
