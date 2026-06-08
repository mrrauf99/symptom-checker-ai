import { Outlet, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Sidebar from './Sidebar.jsx'
import { sessionsAPI } from '../../api/sessionsAPI.js'
import { chatAPI } from '../../api/chatAPI.js'
import toast from 'react-hot-toast'

export default function AppLayout() {
  const [sessions, setSessions] = useState([])
  const navigate = useNavigate()

  const fetchSessions = async () => {
    try {
      const data = await sessionsAPI.getSessions()
      setSessions(data)
    } catch {
      // silently fail — sidebar sessions are non-critical
    }
  }

  useEffect(() => {
    fetchSessions()
  }, [])

  const handleNewChat = async () => {
    try {
      const title = `Chat — ${new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
      const { session_id } = await sessionsAPI.createSession(title)
      await fetchSessions()
      navigate(`/chat/${session_id}`)
    } catch {
      toast.error('Could not create a new session')
    }
  }

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      <Sidebar sessions={sessions} onNewChat={handleNewChat} />
      <main className="flex-1 overflow-y-auto scrollbar-thin animate-fade-in">
        <Outlet context={{ refreshSessions: fetchSessions }} />
      </main>
    </div>
  )
}
