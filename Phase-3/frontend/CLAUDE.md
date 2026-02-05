# Frontend Guidelines

## Stack
- **Framework**: Next.js 16.1.1 (App Router, Turbopack)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Authentication**: Better Auth (`better-auth`) with session management
- **Data fetching**: SWR
- **Chat UI**: OpenAI ChatKit (`@openai/chatkit-react`)
- **Forms**: react-hook-form + zod validation
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Date utilities**: date-fns

## Patterns
- Use server components by default
- Client components only when needed (interactivity) — mark with `"use client"`
- API calls go through the typed client in `/lib/api/`
- Auth state via the `useAuth` hook; route guards in `(app)/layout.tsx`

## Component Structure
```
frontend/
├── app/
│   ├── (auth)/              # Public routes (no auth required)
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── (app)/               # Protected routes (auth guard in layout)
│   │   ├── dashboard/page.tsx   # Task management dashboard
│   │   ├── chat/page.tsx        # Conversational AI (ChatKit)
│   │   └── layout.tsx           # Navbar + auth guard
│   ├── api/auth/[...all]/route.ts  # Better Auth handler
│   ├── page.tsx             # Home / redirect
│   └── layout.tsx           # Root layout
├── components/
│   ├── chat/
│   │   └── ChatInterface.tsx    # OpenAI ChatKit wrapper (custom fetch with JWT)
│   ├── features/
│   │   ├── auth/                # LoginForm, SignupForm, UserMenu
│   │   ├── dashboard/           # StatsCard, TaskSummary
│   │   └── tasks/               # TaskList, TaskCard, TaskForm, CreateTaskModal,
│   │                            #   EditTaskModal, FilterControls, SortControls
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   └── Footer.tsx
│   ├── ui/                  # Reusable primitives
│   │   ├── Button.tsx       ├── Card.tsx          ├── Input.tsx
│   │   ├── Select.tsx       ├── Modal.tsx         ├── Badge.tsx
│   │   ├── DatePicker.tsx   ├── SearchInput.tsx   ├── CategoryInput.tsx
│   │   ├── LoadingSpinner.tsx└── Toast.tsx
│   └── providers/
│       └── ToastProvider.tsx
├── lib/
│   ├── api/
│   │   ├── client.ts            # Base APIClient — auto-injects Bearer JWT
│   │   ├── tasks.ts             # Task CRUD functions
│   │   └── conversations.ts     # Conversation API functions
│   ├── auth/
│   │   ├── client.ts            # JWT token storage / retrieval
│   │   └── config.ts            # Better Auth configuration
│   ├── hooks/
│   │   ├── useAuth.ts           # Auth state hook
│   │   ├── useTasks.ts          # SWR-based tasks fetcher
│   │   └── useToast.tsx         # Toast notification hook
│   └── utils/
│       ├── cn.ts                # Tailwind class merger (clsx + tailwind-merge)
│       ├── date-formatting.ts   # Date display helpers
│       ├── priority-colors.ts   # Priority → Tailwind color map
│       └── task-filters.ts      # Client-side filter / sort logic
├── types/
│   ├── task.ts                  # Task, Priority, Recurrence types
│   ├── api.ts                   # API response types
│   └── conversation.ts          # Conversation / Message types
└── contexts/                    # React contexts (if any)
```

## API Client
All backend calls go through the typed client. The base `APIClient` in `lib/api/client.ts` automatically attaches the JWT `Authorization` header.

```typescript
import { api } from '@/lib/api/client'

// Tasks
const tasks = await api.getTasks()
await api.createTask({ title: 'Buy milk', priority: 'high' })

// Conversations (chat)
const conversation = await api.createConversation()
await api.sendMessage(conversation.id, { content: 'Add a task' })
```

## Chat / ChatKit Integration
- The `/chat` page renders `<ChatInterface />`, which wraps `@openai/chatkit-react`
- A custom `fetch` function is passed to ChatKit so every request carries the JWT Bearer token
- The backend endpoint it hits is `/api/v1/chatkit` (streaming) and `/api/v1/chatkit/session`
- `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` must be set (use `local-dev` in development)

## Styling
- Use Tailwind CSS utility classes exclusively — no inline styles
- Merge classes with the `cn()` helper from `lib/utils/cn.ts`
- Follow existing component patterns for consistency

## Environment Variables
Copy `frontend/.env.local.example` to `frontend/.env.local` and fill in values:

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend base URL (default `http://localhost:8000`) |
| `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` | ChatKit domain key (`local-dev` in dev) |
| `DATABASE_URL` | PostgreSQL URL — used by Better Auth at runtime |
| `BETTER_AUTH_SECRET` | Secret for Better Auth sessions (min 32 chars) |
| `BETTER_AUTH_URL` | Frontend origin URL (default `http://localhost:3000`) |

## Running
```bash
npm install
npm run dev          # dev server → http://localhost:3000
npm run build        # production build
npm run lint         # ESLint
```
