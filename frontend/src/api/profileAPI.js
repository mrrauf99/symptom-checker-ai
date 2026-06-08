import apiClient from './client.js'

export const profileAPI = {
  getProfile: async () => {
    const res = await apiClient.get('/profile')
    return res.data
  },

  updateProfile: async (data) => {
    const res = await apiClient.put('/profile', data)
    return res.data
  },
}
