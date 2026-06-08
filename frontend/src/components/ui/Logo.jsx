export default function Logo({ size = 'md', showTagline = false }) {
  const sizes = {
    sm: { icon: 32, title: 'text-lg', tagline: 'text-xs' },
    md: { icon: 40, title: 'text-xl', tagline: 'text-xs' },
    lg: { icon: 52, title: 'text-3xl', tagline: 'text-sm' },
  }
  const s = sizes[size]

  return (
    <div className="flex items-center gap-3">
      <div
        className="rounded-xl bg-gradient-to-br from-mint-400 to-mint-600 flex items-center justify-center shadow-mint flex-shrink-0"
        style={{ width: s.icon, height: s.icon }}
      >
        {/* Heartbeat / pulse icon */}
        <svg
          width={s.icon * 0.55}
          height={s.icon * 0.55}
          viewBox="0 0 24 24"
          fill="none"
        >
          <path
            d="M2 12h4l3-8 4 16 3-8h6"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      <div>
        <div className={`font-display font-bold text-slate-800 leading-tight ${s.title}`}>
          MediSense <span className="text-mint-500">AI</span>
        </div>
        {showTagline && (
          <div className={`font-body text-slate-400 ${s.tagline}`}>
            Smart Symptom Checker
          </div>
        )}
      </div>
    </div>
  )
}
