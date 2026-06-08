import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext.jsx'
import LoginPage from './pages/auth/LoginPage.jsx'
import RegisterPage from './pages/auth/RegisterPage.jsx'
import DashboardPage from './pages/dashboard/DashboardPage.jsx'
import ChatPage from './pages/chat/ChatPage.jsx'
import ProfilePage from './pages/profile/ProfilePage.jsx'
import HistoryPage from './pages/history/HistoryPage.jsx'
import AppLayout from './components/layout/AppLayout.jsx'
import FullPageLoader from './components/ui/FullPageLoader.jsx'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <FullPageLoader />
  return user ? children : <Navigate to="/login" replace />
}

function GuestRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <FullPageLoader />
  return !user ? children : <Navigate to="/dashboard" replace />
}

export default function App() {
  return (
    <Routes>
      {/* Guest routes */}
      <Route path="/login" element={<GuestRoute><LoginPage /></GuestRoute>} />
      <Route path="/register" element={<GuestRoute><RegisterPage /></GuestRoute>} />

      {/* Protected routes */}
      <Route path="/" element={<PrivateRoute><AppLayout /></PrivateRoute>}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="chat" element={<ChatPage />} />
        <Route path="chat/:sessionId" element={<ChatPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="history" element={<HistoryPage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}
