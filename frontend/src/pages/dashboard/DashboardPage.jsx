import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'
import { sessionsAPI } from '../../api/sessionsAPI.js'
import { historyAPI } from '../../api/chatAPI.js'
import { formatRelative } from '../../utils/helpers.js'
import {
  MessageSquare, Plus, Activity, Clock,
  ChevronRight, TrendingUp, Bot, Stethoscope,
} from '../../components/layout/icons.jsx'
import Spinner from '../../components/ui/Spinner.jsx'
import toast from 'react-hot-toast'

function StatCard({ icon: Icon, label, value, color = 'mint' }) {
  const colors = {
    mint: 'bg-mint-50 text-mint-600',
    blue: 'bg-blue-50 text-blue-600',
    amber: 'bg-amber-50 text-amber-600',
  }
  return (
    <div className="card flex items-center gap-4">
      <div className={`w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 ${colors[color]}`}>
        <Icon size={20} />
      </div>
      <div>
        <p className="text-2xl font-display font-bold text-slate-800">{value}</p>
        <p className="text-xs text-slate-500 font-body">{label}</p>
      </div>
    </div>
  )
}

function QuickAction({ icon: Icon, title, subtitle, onClick }) {
  return (
    <button
      onClick={onClick}
      className="card text-left hover:shadow-card-hover hover:border-mint-200 transition-all duration-200 group"
    >
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-mint-50 text-mint-600 flex items-center justify-center flex-shrink-0 group-hover:bg-mint-100 transition-colors">
          <Icon size={18} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-display font-semibold text-slate-800 text-sm">{title}</p>
          <p className="text-xs text-slate-500 font-body mt-0.5">{subtitle}</p>
        </div>
        <ChevronRight size={16} className="text-slate-300 group-hover:text-mint-500 transition-colors mt-0.5" />
      </div>
    </button>
  )
}

export default function DashboardPage() {
  const { user} = useAuth()
  const navigate = useNavigate()

  const [sessions, setSessions] = useState([])
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [s, h] = await Promise.all([
          sessionsAPI.getSessions(),
          historyAPI.getHistory(),
        ])
        setSessions(s)
        setHistory(h)
      } catch {
        // non-blocking
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const handleNewChat = async () => {
    try {
      const title = `Session — ${new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
      const { session_id } = await sessionsAPI.createSession(title)
      navigate(`/chat/${session_id}`)
    } catch {
      toast.error('Could not create session')
    }
  }

  const greeting = () => {
    const h = new Date().getHours()
    if (h < 12) return 'Good morning'
    if (h < 17) return 'Good afternoon'
    return 'Good evening'
  }

  return (
    <div className="p-6 max-w-5xl mx-auto animate-slide-up">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <span className="badge-mint">Dashboard</span>
        </div>
        <h1 className="font-display font-bold text-2xl text-slate-800">
          {greeting()}, <span className="text-mint-600">{user?.name}</span> 👋
        </h1>
        <p className="text-slate-500 font-body text-sm mt-1">
          What symptoms would you like to check today?
        </p>
      </div>

      {/* Start new chat CTA */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-mint-500 to-mint-600 p-6 mb-8 shadow-mint">
        <div className="absolute -right-8 -top-8 w-40 h-40 rounded-full bg-white opacity-5" />
        <div className="absolute -right-4 -bottom-4 w-28 h-28 rounded-full bg-white opacity-5" />
        <div className="relative flex items-center justify-between gap-4">
          <div>
            <h2 className="font-display font-bold text-white text-xl mb-1">
              Describe your symptoms
            </h2>
            <p className="text-mint-100 text-sm font-body">
              Our AI will analyze and suggest possible conditions instantly
            </p>
          </div>
          <button
            onClick={handleNewChat}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-mint-700
              font-display font-semibold text-sm hover:bg-mint-50 transition-colors flex-shrink-0 shadow"
          >
            <Plus size={16} />
            Start Chat
          </button>
        </div>
      </div>

      {/* Stats */}
      {loading ? (
        <div className="flex justify-center py-8">
          <Spinner />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-3 gap-4 mb-8">
            <StatCard icon={MessageSquare} label="Total Sessions" value={sessions.length} color="mint" />
            <StatCard icon={Activity} label="Predictions Made" value={history.length} color="blue" />
            <StatCard icon={TrendingUp} label="Conditions Found" value={[...new Set(history.map(h => h.prediction))].length} color="amber" />
          </div>

          {/* Quick actions */}
          <div className="mb-8">
            <h2 className="font-display font-semibold text-slate-700 text-sm mb-3">Quick Actions</h2>
            <div className="grid grid-cols-2 gap-3">
              <QuickAction
                icon={Bot}
                title="AI Symptom Check"
                subtitle="Describe symptoms, get instant insights"
                onClick={handleNewChat}
              />
              <QuickAction
                icon={Clock}
                title="View History"
                subtitle="Review your past predictions"
                onClick={() => navigate('/history')}
              />
              <QuickAction
                icon={Stethoscope}
                title="Recent Sessions"
                subtitle="Continue a previous conversation"
                onClick={() => navigate('/chat')}
              />
              <QuickAction
                icon={Activity}
                title="Update Profile"
                subtitle="Keep your health info current"
                onClick={() => navigate('/profile')}
              />
            </div>
          </div>

          {/* Recent sessions */}
          {sessions.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-3">
                <h2 className="font-display font-semibold text-slate-700 text-sm">Recent Conversations</h2>
                <button
                  onClick={() => navigate('/history')}
                  className="text-xs text-mint-600 font-body font-medium hover:text-mint-700"
                >
                  View all
                </button>
              </div>
              <div className="flex flex-col gap-2">
                {sessions.slice(0, 5).map((s) => (
                  <button
                    key={s.id}
                    onClick={() => navigate(`/chat/${s.id}`)}
                    className="flex items-center gap-3 p-3.5 rounded-xl bg-white border border-slate-100
                      hover:border-mint-200 hover:shadow-card transition-all duration-200 text-left group"
                  >
                    <div className="w-8 h-8 rounded-lg bg-mint-50 flex items-center justify-center flex-shrink-0">
                      <MessageSquare size={14} className="text-mint-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-body font-medium text-slate-800 text-sm truncate">{s.title}</p>
                      <p className="text-xs text-slate-400 font-body">{formatRelative(s.created_at)}</p>
                    </div>
                    <ChevronRight size={14} className="text-slate-300 group-hover:text-mint-500 transition-colors" />
                  </button>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
