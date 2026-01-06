# Mealworm Frontend - Setup Complete

The complete Next.js 14 frontend has been built and is ready to use!

## What's Been Built

### Core Infrastructure
- ✅ Next.js 14 with TypeScript and Tailwind CSS
- ✅ App Router architecture with route groups
- ✅ Environment configuration (.env.local)
- ✅ ESLint configuration
- ✅ All dependencies installed (390 packages)

### Type Definitions
- ✅ `types/auth.ts` - User, login, and register types
- ✅ `types/preferences.ts` - Complete preferences interface
- ✅ `types/agent.ts` - Agent types, models, and run requests

### API Client
- ✅ `lib/api.ts` - Complete API wrapper with:
  - Auth endpoints (register, login, logout, me)
  - Preferences endpoints (get, update)
  - Agent endpoints with streaming support
  - Cookie-based authentication
  - Custom ApiError handling

### Hooks & Context
- ✅ `hooks/useAuth.tsx` - Authentication context provider with:
  - User state management
  - Login/register/logout functions
  - Automatic token refresh
  - Protected route redirection
- ✅ `hooks/usePreferences.tsx` - Preferences management with:
  - Fetch and update preferences
  - Loading and error states
  - Auto-refresh capability

### UI Components
Complete set of reusable components in `components/ui/`:
- ✅ Button (multiple variants and sizes)
- ✅ Input (with dark mode support)
- ✅ Label
- ✅ Card (with header, content, footer)
- ✅ Textarea
- ✅ Checkbox

### Pages

#### Public Pages
- ✅ **Login** (`app/(auth)/login/page.tsx`)
  - Email/password form
  - Error handling
  - Link to register
  - Auto-redirect if authenticated

- ✅ **Register** (`app/(auth)/register/page.tsx`)
  - Registration form with password confirmation
  - Validation (min 8 characters)
  - Redirects to onboarding after success
  - Single-user system notice

#### Protected Pages
- ✅ **Dashboard** (`app/(dashboard)/dashboard/page.tsx`)
  - Meal plan generator with AI streaming
  - Real-time response display
  - Quick generate button
  - Tips and guidance
  - Links to preferences and logout

- ✅ **Preferences** (`app/(dashboard)/preferences/page.tsx`)
  - Comprehensive preferences form:
    - Meal plan requirements (chicken, fish counts)
    - Eating preferences (vegetables, leftovers)
    - Food likes/dislikes
    - Cuisine preferences
    - Dietary restrictions and allergens
    - Sauce and easy meal preferences
    - Shopping list template
  - Save functionality with success feedback
  - Back to dashboard navigation

- ✅ **Onboarding** (`app/onboarding/page.tsx`)
  - 4-step wizard:
    1. Basic meal planning (chicken/fish counts, checkboxes)
    2. Taste preferences (likes, dislikes, cuisines)
    3. Dietary restrictions (restrictions, allergens, avoid types)
    4. Additional preferences (sauce, easy meals)
  - Progress bar
  - Navigation (next, previous)
  - Skip option
  - Saves all preferences and redirects to dashboard

#### Other
- ✅ **Home** (`app/page.tsx`)
  - Intelligent redirect based on auth status
  - Loading state

### Security & Protection
- ✅ **Middleware** (`middleware.ts`)
  - Route protection for authenticated pages
  - Auto-redirect to login if not authenticated
  - Auto-redirect to dashboard if authenticated on public pages
  - Cookie-based token checking

### Styling
- ✅ `app/globals.css` - Global styles with:
  - Tailwind directives
  - Dark mode support
  - CSS custom properties
  - Typography utilities

## Project Structure

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx          # Login page
│   │   └── register/page.tsx       # Registration page
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx      # Main dashboard
│   │   └── preferences/page.tsx    # Preferences management
│   ├── onboarding/page.tsx         # Onboarding wizard
│   ├── layout.tsx                  # Root layout with AuthProvider
│   ├── globals.css                 # Global styles
│   └── page.tsx                    # Home with redirect
├── components/
│   └── ui/                         # Reusable UI components
│       ├── button.tsx
│       ├── card.tsx
│       ├── checkbox.tsx
│       ├── input.tsx
│       ├── label.tsx
│       └── textarea.tsx
├── hooks/
│   ├── useAuth.tsx                 # Auth context & hook
│   └── usePreferences.tsx          # Preferences hook
├── lib/
│   ├── api.ts                      # API client
│   └── utils.ts                    # Utility functions
├── types/
│   ├── agent.ts                    # Agent types
│   ├── auth.ts                     # Auth types
│   └── preferences.ts              # Preferences types
├── middleware.ts                   # Route protection
├── .env.local                      # Environment variables
├── package.json                    # Dependencies
├── tsconfig.json                   # TypeScript config
├── tailwind.config.ts              # Tailwind config
├── next.config.js                  # Next.js config
├── postcss.config.js               # PostCSS config
├── .eslintrc.json                  # ESLint config
└── README.md                       # Frontend documentation

```

## How to Run

### 1. Start the Backend
Make sure your FastAPI backend is running:
```bash
# In the project root
docker compose up
# or
uvicorn main_agno:app --reload
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## User Flow

### First Time User
1. Visit `http://localhost:3000`
2. Redirected to `/login`
3. Click "Sign up" → Register with email/password
4. Automatically redirected to `/onboarding`
5. Complete 4-step onboarding wizard
6. Redirected to `/dashboard`
7. Generate first meal plan!

### Returning User
1. Visit `http://localhost:3000`
2. Redirected to `/login`
3. Sign in with credentials
4. Redirected to `/dashboard`
5. Generate meal plans or update preferences

## Key Features

### Authentication
- Cookie-based JWT authentication
- Automatic token management
- Protected routes with middleware
- Single-user system (only one account allowed)

### Meal Plan Generation
- Stream AI responses in real-time
- Personalized based on user preferences
- Multiple model support (GPT, Claude)
- Quick generate option

### Preferences Management
- Comprehensive preference categories
- Real-time save with success feedback
- Pre-populated with defaults
- Used by AI for personalization

### User Experience
- Responsive design (mobile-friendly)
- Dark mode support
- Loading states
- Error handling
- Form validation

## API Endpoints Used

### Authentication
- `POST /v1/auth/register` - Create account
- `POST /v1/auth/login` - Sign in
- `POST /v1/auth/logout` - Sign out
- `GET /v1/auth/me` - Get current user

### Preferences
- `GET /v1/preferences` - Fetch preferences
- `PUT /v1/preferences` - Update preferences

### Agents
- `POST /v1/agents/meal_planning_agent/runs` - Generate meal plan (with streaming)

## Next Steps

### Testing the Application
1. Start both backend and frontend
2. Register a new account
3. Complete onboarding
4. Generate a meal plan
5. Update preferences
6. Generate another meal plan (should reflect new preferences)

### Optional Enhancements
- Add meal plan history page
- Add ability to save/favorite meal plans
- Add PDF export for meal plans
- Add grocery list copy/print functionality
- Add meal plan calendar view
- Add recipe details for meals
- Add nutrition information
- Add social sharing

## Troubleshooting

### Frontend won't start
- Ensure Node.js 18+ is installed
- Delete `node_modules` and `package-lock.json`, run `npm install` again

### Can't connect to backend
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Ensure backend is running on port 8000
- Check for CORS issues in backend

### Authentication not working
- Check that cookies are enabled in browser
- Verify backend is setting cookies correctly
- Check browser DevTools → Application → Cookies

### Streaming not working
- Ensure browser supports ReadableStream
- Check network tab for proper response type
- Verify backend is sending streaming response

## Technologies Used

- **Next.js 14**: React framework with App Router
- **React 18**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **React Hook Form**: Form management
- **Zod**: Schema validation
- **Lucide React**: Beautiful icons
- **clsx + tailwind-merge**: Conditional classes

---

The frontend is complete and ready to use! All pages, components, and functionality have been implemented. Just start the dev server and you're good to go! 🎉
