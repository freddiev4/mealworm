# Mealworm Frontend

AI-powered meal planning application built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

- **Authentication**: Secure login and registration with JWT cookies
- **Onboarding Flow**: Multi-step wizard to set up user preferences
- **Dashboard**: Interactive meal plan generator with AI streaming responses
- **Preferences Management**: Comprehensive form to customize meal planning
- **Route Protection**: Middleware-based authentication guard
- **Responsive Design**: Mobile-friendly UI with Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`.

### Environment Variables

Create a `.env.local` file with:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── app/                      # Next.js 14 App Router
│   ├── (auth)/              # Authentication pages (login, register)
│   ├── (dashboard)/         # Protected dashboard pages
│   ├── onboarding/          # Onboarding wizard
│   ├── layout.tsx           # Root layout with AuthProvider
│   └── page.tsx             # Home page with redirect logic
├── components/              # Reusable UI components
│   └── ui/                  # Base UI components (button, input, card, etc.)
├── hooks/                   # Custom React hooks
│   ├── useAuth.tsx          # Authentication context and hook
│   └── usePreferences.tsx   # Preferences fetching and updating
├── lib/                     # Utility functions
│   ├── api.ts              # API client with fetch wrapper
│   └── utils.ts            # Helper functions
├── types/                   # TypeScript type definitions
│   ├── auth.ts             # User and auth types
│   ├── preferences.ts      # User preferences types
│   └── agent.ts            # Agent and meal planning types
└── middleware.ts           # Route protection middleware

```

## Available Routes

### Public Routes
- `/login` - Sign in page
- `/register` - Registration page (single-user system)

### Protected Routes
- `/dashboard` - Main dashboard with meal plan generator
- `/preferences` - Preferences management
- `/onboarding` - First-time setup wizard

## Key Technologies

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **React Hook Form**: Form state management
- **Zod**: Schema validation
- **Lucide React**: Icon library

## API Integration

The frontend communicates with the backend via:
- **Auth API**: `/v1/auth/*` - Login, register, logout, user info
- **Preferences API**: `/v1/preferences` - Get/update preferences
- **Agent API**: `/v1/agents/*` - Generate meal plans with streaming

All requests include credentials for cookie-based authentication.

## Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

## Features Overview

### Authentication Flow
1. User registers (single-user system allows only one account)
2. JWT token stored in httpOnly cookie
3. Redirected to onboarding flow
4. After onboarding, access to dashboard

### Meal Plan Generation
1. User enters prompt in dashboard
2. Request sent to agent API with streaming enabled
3. Response chunks displayed in real-time
4. User can save or regenerate plans

### Preferences Management
- Weekly meal requirements (chicken, fish, etc.)
- Food likes/dislikes
- Cuisine preferences
- Dietary restrictions and allergens
- Shopping list template items
- Sauce and easy meal preferences

## License

See parent project LICENSE file.
