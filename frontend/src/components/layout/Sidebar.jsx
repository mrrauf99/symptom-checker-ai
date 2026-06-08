import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'
import Logo from '../ui/Logo.jsx'
import toast from 'react-hot-toast'
import {
  LayoutDashboard,
  MessageSquare,
  Clock,
  User,
  LogOut,
  Plus,
} from './icons.jsx'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/chat', icon: MessageSquare, label: 'New Chat' },
  { to: '/history', icon: Clock, label: 'History' },
  { to: '/profile', icon: User, label: 'Profile' },
]

export default function Sidebar({ sessions = [], onNewChat }) {
  const { logout, user } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  return (
    <aside className="w-64 h-full bg-white border-r border-slate-100 flex flex-col">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-slate-100">
        <Logo size="sm" />
      </div>

      {/* New Chat Button */}
      <div className="px-4 pt-4">
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-2 px-4 py-2.5 rounded-xl
            bg-mint-500 hover:bg-mint-600 text-white text-sm font-display font-semibold
            shadow-mint transition-all duration-200"
        >
          <Plus size={16} />
          New Conversation
        </button>
      </div>

      {/* Navigation */}
      <nav className="px-3 pt-4 flex flex-col gap-0.5">
        <p className="px-3 pb-1 text-xs font-display font-semibold text-slate-400 uppercase tracking-wider">
          Menu
        </p>
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `sidebar-item ${isActive ? 'sidebar-item-active' : ''}`
            }
          >
            <Icon size={17} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Recent Sessions */}
      {sessions.length > 0 && (
        <div className="px-3 pt-4 flex-1 overflow-hidden flex flex-col">
          <p className="px-3 pb-1 text-xs font-display font-semibold text-slate-400 uppercase tracking-wider">
            Recent Chats
          </p>
          <div className="flex flex-col gap-0.5 overflow-y-auto scrollbar-thin flex-1">
            {sessions.slice(0, 10).map((s) => (
              <NavLink
                key={s.id}
                to={`/chat/${s.id}`}
                className={({ isActive }) =>
                  `sidebar-item truncate ${isActive ? 'sidebar-item-active' : ''}`
                }
              >
                <MessageSquare size={14} className="flex-shrink-0" />
                <span className="truncate text-xs">{s.title}</span>
              </NavLink>
            ))}
          </div>
        </div>
      )}

      {/* User + Logout */}
      <div className="mt-auto border-t border-slate-100 px-4 py-4">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-mint-100 flex items-center justify-center text-mint-700 font-display font-semibold text-sm flex-shrink-0">
            {user?.email?.[0]?.toUpperCase() || 'U'}
          </div>
          <div className="min-w-0">
            <p className="text-xs font-display font-semibold text-slate-700 truncate">
              {user?.email}
            </p>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-slate-500
            hover:bg-rose-50 hover:text-rose-600 text-sm font-body font-medium transition-all duration-200"
        >
          <LogOut size={15} />
          Sign out
        </button>
      </div>
    </aside>
  )
}
