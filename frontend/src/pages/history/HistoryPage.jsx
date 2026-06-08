import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { sessionsAPI } from '../../api/sessionsAPI.js'
import { formatDate, formatTime, getErrorMessage } from '../../utils/helpers.js'
import { MessageSquare, Search, Calendar, AlertCircle, Clock } from '../../components/layout/icons.jsx'
import Spinner from '../../components/ui/Spinner.jsx'
import toast from 'react-hot-toast'

function SessionItem({ session, index }) {
  return (
    <Link to={`/chat/${session.id}`} className="block">
      <div
        className="card hover:shadow-card-hover hover:border-mint-200 transition-all duration-200 animate-slide-up cursor-pointer"
        style={{ animationDelay: `${index * 40}ms` }}
      >
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-xl bg-mint-50 flex items-center justify-center flex-shrink-0 text-mint-600">
            <MessageSquare size={20} />
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-slate-800 font-display font-semibold text-base truncate pr-4">
                {session.title || "Untitled Session"}
              </h3>
              <span className={`px-2.5 py-1 rounded-full text-[10px] font-display font-bold uppercase tracking-wider ${
                session.status === 'completed' 
                  ? 'bg-slate-100 text-slate-500' 
                  : 'bg-mint-100 text-mint-700'
              }`}>
                {session.status || 'active'}
              </span>
            </div>

            <div className="flex items-center gap-4 flex-wrap text-xs text-slate-500 font-body">
              <span className="flex items-center gap-1.5">
                <Calendar size={12} className="text-slate-400" />
                Created: {formatDate(session.created_at)} at {formatTime(session.created_at)}
              </span>
              <span className="flex items-center gap-1.5">
                <Clock size={12} className="text-slate-400" />
                Last Activity: {formatDate(session.updated_at)} at {formatTime(session.updated_at)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  )
}

function EmptySessions() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
        <MessageSquare size={28} className="text-slate-400" />
      </div>
      <h3 className="font-display font-semibold text-slate-700 text-lg mb-2">No chat sessions yet</h3>
      <p className="text-slate-400 font-body text-sm max-w-xs mb-6">
        Your chat sessions will appear here once you start analyzing symptoms.
      </p>
      <Link to="/chat" className="btn-primary">
        Start a new chat
      </Link>
    </div>
  )
}

export default function HistoryPage() {
  const [sessions, setSessions] = useState([])
  const [filtered, setFiltered] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await sessionsAPI.getSessions()
        // API returns already sorted by updated_at desc
        setSessions(data)
        setFiltered(data)
      } catch (err) {
        toast.error(getErrorMessage(err))
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  useEffect(() => {
    if (!search.trim()) {
      setFiltered(sessions)
      return
    }
    const q = search.toLowerCase()
    setFiltered(
      sessions.filter(
        (s) => s.title?.toLowerCase().includes(q)
      )
    )
  }, [search, sessions])

  const completedCount = sessions.filter(s => s.status === 'completed').length

  return (
    <div className="p-6 max-w-3xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <span className="badge-mint mb-2">Records</span>
        <h1 className="font-display font-bold text-2xl text-slate-800">Chat Sessions History</h1>
        <p className="text-slate-500 font-body text-sm mt-1">
          Review your previous conversations and analyses.
        </p>
      </div>

      {/* Summary cards */}
      {!loading && sessions.length > 0 && (
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="card">
            <p className="text-2xl font-display font-bold text-slate-800">{sessions.length}</p>
            <p className="text-xs text-slate-500 font-body">Total Sessions</p>
          </div>
          <div className="card">
            <p className="text-2xl font-display font-bold text-mint-600">{completedCount}</p>
            <p className="text-xs text-slate-500 font-body">Completed Sessions</p>
          </div>
        </div>
      )}

      {/* Search */}
      {!loading && sessions.length > 0 && (
        <div className="relative mb-6">
          <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
            <Search size={15} />
          </span>
          <input
            type="text"
            placeholder="Search sessions by title..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-base pl-10"
          />
        </div>
      )}

      {/* Content */}
      {loading ? (
        <div className="flex justify-center py-16">
          <Spinner />
        </div>
      ) : sessions.length === 0 ? (
        <EmptySessions />
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center py-16 text-center gap-3">
          <AlertCircle size={32} className="text-slate-300" />
          <p className="text-slate-500 font-body text-sm">No sessions found matching "{search}"</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((session, i) => (
            <SessionItem key={session.id} session={session} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}
