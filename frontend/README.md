# MediSense AI — Frontend

> Smart symptom checker powered by AI. Built with React + Vite + Tailwind CSS.

## Tech Stack

- **React 18** + Vite
- **Tailwind CSS** (custom design system)
- **React Router v6** (App Router pattern)
- **Axios** (API client with interceptors)
- **React Hot Toast** (notifications)
- **Sora + DM Sans** (custom typography)

## Project Structure

```
src/
├── api/               # All API call functions (per domain)
│   ├── client.js      # Axios instance + interceptors
│   ├── authAPI.js
│   ├── chatAPI.js
│   ├── messagesAPI.js
│   ├── profileAPI.js
│   └── sessionsAPI.js
├── components/
│   ├── ui/            # Reusable atoms (Input, Button, Spinner, Logo)
│   └── layout/        # Structural components (Sidebar, AppLayout, AuthLayout, icons)
├── context/
│   └── AuthContext.jsx  # Global auth state + JWT management
├── hooks/             # Custom hooks (reserved for expansion)
├── pages/             # One folder per route
│   ├── auth/          # Login, Register
│   ├── dashboard/     # Dashboard
│   ├── chat/          # Chat interface
│   ├── profile/       # Profile management
│   └── history/       # Prediction history
├── styles/
│   └── index.css      # Tailwind base + component classes
└── utils/
    ├── validators.js  # Form validation rules
    └── helpers.js     # Date formatters, error extractors
```

## Getting Started

```bash
# 1. Install dependencies
npm install

# 2. Set up environment
cp .env.example .env
# Edit .env and set VITE_API_URL to your backend

# 3. Start development server
npm run dev
# → http://localhost:3000

# 4. Build for production
npm run build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend base URL | `http://localhost:8000` |

## Pages & Routes

| Route | Page | Auth Required |
|-------|------|---------------|
| `/login` | Login | No |
| `/register` | Register | No |
| `/dashboard` | Dashboard | Yes |
| `/chat` | New Chat | Yes |
| `/chat/:sessionId` | Chat Session | Yes |
| `/profile` | Profile | Yes |
| `/history` | History | Yes |

## Design System

Colors are defined in `tailwind.config.js`:
- **Mint** (`mint-*`) — primary brand color (green-teal)
- **Slate** (`slate-*`) — neutrals / text
- **Coral** (`coral-*`) — errors / danger states

Component classes are defined in `src/styles/index.css`:
- `.input-base`, `.input-error` — form inputs
- `.btn-primary`, `.btn-secondary`, `.btn-ghost` — buttons
- `.card` — elevated card container
- `.badge`, `.badge-mint`, `.badge-coral` — labels
- `.sidebar-item`, `.sidebar-item-active` — nav items

## Notes

- JWT is stored in `localStorage` under the key `"token"`
- 401 responses automatically redirect to `/login` via Axios interceptor
- All form validation is client-side first, with server errors surfaced via toast
- The AI disclaimer is shown in every chat view — never remove it
