import apiClient from './client.js'

export const chatAPI = {
  sendMessage: async (data) => {
    const res = await apiClient.post('/chat/send', data)
    return res.data
  },
}

export const historyAPI = {
  getHistory: async () => {
    const res = await apiClient.get('/history')
    return res.data
  },
}
