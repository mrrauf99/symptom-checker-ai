import Logo from '../ui/Logo.jsx'

export default function AuthLayout({ children, title, subtitle }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-mint-50 via-slate-50 to-slate-100 flex items-center justify-center p-4">
      {/* Decorative background shapes */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-mint-100 opacity-40 blur-3xl" />
        <div className="absolute -bottom-32 -left-32 w-80 h-80 rounded-full bg-mint-200 opacity-30 blur-3xl" />
        <div className="absolute top-1/2 left-1/4 w-64 h-64 rounded-full bg-slate-200 opacity-20 blur-2xl" />
      </div>

      <div className="relative w-full max-w-md">
        {/* Card */}
        <div className="bg-white rounded-3xl shadow-card-hover border border-slate-100 p-8 animate-slide-up">
          {/* Logo */}
          <div className="flex justify-center mb-8">
            <Logo size="md" showTagline />
          </div>

          {/* Title */}
          <div className="text-center mb-8">
            <h1 className="font-display font-bold text-2xl text-slate-800 mb-1.5">{title}</h1>
            <p className="font-body text-slate-500 text-sm">{subtitle}</p>
          </div>

          {children}
        </div>

        {/* Trust badges */}
        <div className="flex items-center justify-center gap-6 mt-5 text-xs text-slate-400 font-body">
          <span className="flex items-center gap-1.5">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M6 1L7.5 4.5H11L8.5 6.5L9.5 10L6 8L2.5 10L3.5 6.5L1 4.5H4.5L6 1Z" fill="#22c48a" />
            </svg>
            AI-Powered
          </span>
          <span className="flex items-center gap-1.5">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <rect x="2" y="5" width="8" height="6" rx="1" stroke="#22c48a" strokeWidth="1.2" />
              <path d="M4 5V3.5a2 2 0 0 1 4 0V5" stroke="#22c48a" strokeWidth="1.2" strokeLinecap="round" />
            </svg>
            Secure & Private
          </span>
          <span className="flex items-center gap-1.5">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <circle cx="6" cy="6" r="5" stroke="#22c48a" strokeWidth="1.2" />
              <path d="M4 6l1.5 1.5L8 4.5" stroke="#22c48a" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            Free to Use
          </span>
        </div>
      </div>
    </div>
  )
}
