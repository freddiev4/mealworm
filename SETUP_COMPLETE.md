# Mealworm Setup Complete! 🎉

Your complete meal planning application with authentication is now running!

## What's Running

### Backend API ✅
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Status**: Running with authentication enabled
- **Database**: PostgreSQL with pgvector extension
- **Migrations**: Applied successfully

### Frontend Web App ✅
- **URL**: http://localhost:3000
- **Framework**: Next.js 14 with TypeScript
- **Status**: Running in development mode

## What Was Built

### Backend Features
- ✅ JWT authentication with PyJWT (switched from python-jose for simpler dependencies)
- ✅ User registration (single-user system)
- ✅ User login/logout with httpOnly cookies
- ✅ User preferences management
- ✅ Protected agent endpoints
- ✅ Database models for users, preferences, and meal plans
- ✅ Alembic migrations

### Frontend Features
- ✅ Complete authentication UI (login, register)
- ✅ 4-step onboarding wizard
- ✅ Dashboard with AI meal plan generator
- ✅ Real-time streaming responses from AI
- ✅ Comprehensive preferences management page
- ✅ Route protection middleware
- ✅ Responsive design with Tailwind CSS

## How to Use

### First Time Setup
1. Open http://localhost:3000 in your browser
2. Click "Sign up" to create your account
3. Complete the onboarding wizard (4 steps):
   - Basic meal planning preferences
   - Taste preferences (likes, dislikes, cuisines)
   - Dietary restrictions
   - Additional preferences
4. You'll be redirected to the dashboard

### Generate a Meal Plan
1. In the dashboard, enter a prompt like:
   - "Generate me a meal plan for next week"
   - "Create a meal plan with more Asian dishes"
   - "I want easy meals this week"
2. Click "Generate" or use "Quick Generate"
3. Watch the AI stream the response in real-time
4. Your preferences are automatically used to personalize the plan

### Update Preferences
1. Click "Preferences" in the header
2. Update any of your preferences:
   - Weekly meal requirements
   - Food likes/dislikes
   - Cuisines
   - Dietary restrictions
   - Shopping list items
3. Click "Save Preferences"
4. Generate a new meal plan to see the changes reflected

## Technical Details

### Dependency Resolution Fix
We switched from `python-jose` to `PyJWT` because:
- PyJWT is already in your requirements (simpler)
- Fewer transitive dependencies
- Works better with `uv pip sync`
- No need for extras like `ecdsa`, `six`, `markupsafe`

### Database Tables Created
- `users` - User accounts (email, hashed password)
- `user_preferences` - Meal planning preferences
- `generated_meal_plans` - Historical meal plans (for future features)

### API Endpoints

#### Authentication
- `POST /v1/auth/register` - Create account
- `POST /v1/auth/login` - Sign in
- `POST /v1/auth/logout` - Sign out
- `GET /v1/auth/me` - Get current user

#### Preferences
- `GET /v1/preferences` - Fetch preferences
- `PUT /v1/preferences` - Update preferences

#### Agents
- `POST /v1/agents/meal_planning_agent/runs` - Generate meal plan (requires auth)

## Project Structure

```
mealworm/
├── mealworm/                    # Backend
│   ├── api/
│   │   ├── auth/               # JWT & auth dependencies
│   │   └── routes/             # API endpoints
│   ├── agents/                 # AI agents
│   └── db/                     # Database models
├── frontend/                    # Frontend
│   ├── app/                    # Next.js pages
│   ├── components/             # UI components
│   ├── hooks/                  # React hooks
│   ├── lib/                    # API client
│   └── types/                  # TypeScript types
└── alembic/                    # Database migrations
```

## Commands

### Backend
```bash
# View logs
docker compose logs -f api

# Run migrations
docker compose exec api alembic upgrade head

# Create new migration
docker compose exec api alembic revision --autogenerate -m "Description"

# Restart backend
docker compose restart api
```

### Frontend
```bash
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Run production build
npm start
```

## Troubleshooting

### Backend Issues
- **Check logs**: `docker compose logs api --tail 50`
- **Restart**: `docker compose restart api`
- **Rebuild**: `docker compose up --build -d`

### Frontend Issues
- **Port conflict**: Stop any process on port 3000
- **Dependency issues**: `cd frontend && rm -rf node_modules && npm install`
- **Check connection**: Verify backend is running on port 8000

### Authentication Issues
- **Clear cookies**: Open DevTools → Application → Cookies → Clear
- **Check JWT_SECRET_KEY**: Verify `.env` has `JWT_SECRET_KEY` set
- **Database**: Ensure migrations ran successfully

## Next Steps

### Immediate
- Test the registration/login flow
- Complete onboarding
- Generate your first meal plan
- Update preferences and regenerate

### Future Enhancements
- Meal plan history page
- Save/favorite meal plans
- PDF export
- Grocery list copy/print
- Meal plan calendar view
- Recipe details
- Nutrition information
- Social sharing

## Environment Variables

### Backend (.env)
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mealworm
DB_USER=postgres
DB_PASSWORD=postgres
JWT_SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Files Documentation

- `FRONTEND_SETUP.md` - Detailed frontend documentation
- `frontend/README.md` - Frontend project README
- `requirements.txt` - Python dependencies (140 packages)
- `package.json` - Node.js dependencies (390 packages)

---

🎉 **Everything is ready to use!** Open http://localhost:3000 and start meal planning!

For issues or questions, check the logs or refer to the documentation files.
