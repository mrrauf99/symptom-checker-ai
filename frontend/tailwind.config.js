/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['Sora', 'sans-serif'],
        body: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        mint: {
          50:  '#f0fdf8',
          100: '#dcfcf0',
          200: '#bbf7e1',
          300: '#86efcb',
          400: '#4adea9',
          500: '#22c48a',
          600: '#16a370',
          700: '#15815b',
          800: '#166649',
          900: '#15543d',
        },
        slate: {
          50:  '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        coral: {
          400: '#fb7185',
          500: '#f43f5e',
          600: '#e11d48',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
        'spin-slow': 'spin 1.5s linear infinite',
        'bounce-dot': 'bounceDot 1.2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
        bounceDot: {
          '0%, 80%, 100%': { transform: 'translateY(0)' },
          '40%': { transform: 'translateY(-6px)' },
        },
      },
      boxShadow: {
        'card': '0 2px 16px 0 rgba(16, 30, 54, 0.07)',
        'card-hover': '0 8px 32px 0 rgba(16, 30, 54, 0.12)',
        'mint': '0 4px 24px 0 rgba(34, 196, 138, 0.25)',
      },
    },
  },
  plugins: [],
}
