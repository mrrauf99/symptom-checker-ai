export default function Input({
  label,
  id,
  error,
  icon: Icon,
  rightElement,
  className = '',
  ...props
}) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label
          htmlFor={id}
          className="text-sm font-display font-medium text-slate-700"
        >
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
            <Icon size={16} />
          </span>
        )}
        <input
          id={id}
          className={`input-base ${Icon ? 'pl-10' : ''} ${rightElement ? 'pr-12' : ''} ${
            error ? 'input-error' : ''
          } ${className}`}
          {...props}
        />
        {rightElement && (
          <span className="absolute right-3.5 top-1/2 -translate-y-1/2">
            {rightElement}
          </span>
        )}
      </div>
      {error && (
        <p className="text-xs text-coral-500 font-body flex items-center gap-1 animate-fade-in">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <circle cx="6" cy="6" r="5.5" stroke="#f43f5e" />
            <path d="M6 3.5V6.5" stroke="#f43f5e" strokeLinecap="round" />
            <circle cx="6" cy="8.5" r="0.5" fill="#f43f5e" />
          </svg>
          {error}
        </p>
      )}
    </div>
  )
}
