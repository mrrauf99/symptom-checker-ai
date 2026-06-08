import apiClient from './client.js'

export const authAPI = {
  register: async (data) => {
    const res = await apiClient.post('/auth/register', data)
    return res.data
  },

  login: async (data) => {
    const res = await apiClient.post('/auth/login', data)
    const { access_token } = res.data
    localStorage.setItem('token', access_token)
    return res.data
  },

  me: async () => {
    const res = await apiClient.get('/auth/me')
    return res.data
  },

  logout: () => {
    localStorage.removeItem('token')
  },
}
