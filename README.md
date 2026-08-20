# ResumeAI

> Build ATS-friendly resumes, check them against job descriptions, and improve them with AI.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20ResumeAI-2563eb?style=for-the-badge)](https://resume-ai-seven-chi.vercel.app/)

**[Explore the live demo →](https://resume-ai-seven-chi.vercel.app/)**

ResumeAI is a Django application for professional resume building, ATS analysis, and AI-assisted career guidance. It uses PostgreSQL in production and is deployed on Vercel.

## Live Demo

Try the deployed app at **[resume-ai-seven-chi.vercel.app](https://resume-ai-seven-chi.vercel.app/)**.

> Create your own account before adding personal resume information.

## Features

| Feature | What it does |
| --- | --- |
| Resume Builder | Create ATS-friendly resumes with live preview and PDF export. |
| ATS Score Checker | Analyze keywords, sections, formatting, readability, and recommendations. |
| AI Career Assistant | Improve bullet points, generate summaries, and tailor resumes through OpenRouter. |
| Authentication | Sign in with email/password or Google OAuth. |
| Google Drive | Store resume files in a connected Google Drive account. |
| Admin Panel | Manage users, templates, scoring, AI settings, and usage from Django Admin. |

## Technology

`Django` · `Django REST Framework` · `PostgreSQL` · `Vercel` · `WhiteNoise` · `django-allauth` · `OpenRouter` · `ReportLab`

---

## Quick Start (Local Development)

### 1. Clone and create venv
```bash
git clone <your-repo>
cd <project>
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and fill in your values
```

### 4. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | No | `True` for dev, `False` for prod |
| `DATABASE_URL` | No | PostgreSQL URL (SQLite used if not set) |
| `GOOGLE_CLIENT_ID` | For OAuth | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | For OAuth | Google OAuth client secret |
| `OPENROUTER_API_KEY` | For AI | OpenRouter API key |
| `OPENROUTER_DEFAULT_MODEL` | No | Default model (e.g. `openai/gpt-4o-mini`) |
| `AI_MAX_REQUESTS_PER_DAY` | No | Daily AI limit per user (default: 50) |
| `EMAIL_HOST` | For email | SMTP host |
| `EMAIL_HOST_USER` | For email | SMTP username |
| `EMAIL_HOST_PASSWORD` | For email | SMTP password |

---

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new OAuth 2.0 Client ID (Web application)
3. Add Authorized redirect URI:
   - Local: `http://127.0.0.1:8000/accounts/google/login/callback/`
   - Production: `https://resume-ai-seven-chi.vercel.app/accounts/google/login/callback/`
4. Enable the **Google Drive API** in your project
5. Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to your `.env`
6. In Django Admin → Sites → Update domain to your domain
7. In Django Admin → Social Applications → Add Google app with your credentials

---

## OpenRouter AI Setup

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Create an API key
3. Add `OPENROUTER_API_KEY` to your `.env`
4. Optionally set `OPENROUTER_DEFAULT_MODEL` (default: `openai/gpt-4o-mini`)

Admins can also override the API key and model via **Django Admin → App Settings**.

---

## Vercel Deployment

### 1. Set up PostgreSQL
Use [Neon](https://neon.tech), [Supabase](https://supabase.com), or [Railway](https://railway.app) for a free PostgreSQL database.

### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/ats-resume-builder.git
git push -u origin main
```

### 3. Deploy on Vercel
1. Go to [vercel.com](https://vercel.com) → **Add New** → **Project** → import this GitHub repository.
2. Set **Framework Preset** to `Other`; keep the root directory at the repository root.
3. Add Production environment variables before deploying:

   ```text
   SECRET_KEY=<long random secret>
   DEBUG=False
   DATABASE_URL=<fresh PostgreSQL connection URL>
   ALLOWED_HOSTS=.vercel.app
   SITE_DOMAIN=resume-ai-seven-chi.vercel.app
   CORS_ALLOWED_ORIGINS=https://resume-ai-seven-chi.vercel.app
   ```

4. Deploy. `vercel.json` and `build_files.sh` configure the build, migrations, static files, and initial seed data—do not add a separate build command or output directory in Project Settings.

### 4. After first deploy
```bash
# Create superuser (run once via Vercel CLI or Railway shell)
python manage.py createsuperuser
```

### Key Vercel Notes
- Vercel's filesystem is **ephemeral** — all files are stored in Google Drive and PostgreSQL, never local disk
- Static files are served via **WhiteNoise** (built into the Django app)
- Serverless functions have a 10-second timeout on the free plan — ensure DB connections are fast

---

## Admin Panel

Access at `/admin/` with superuser credentials.

**What you can manage:**
- Users — view, activate/deactivate, reset AI limits
- Resume Templates — add/edit/disable templates
- ATS Configuration — adjust scoring weights
- App Settings — override OpenRouter API key, model, daily limits **without redeploying**
- AI Usage Logs — monitor token usage
- Job Descriptions — view user JDs
- Drive Files — view stored file metadata
- Social Applications — configure Google OAuth

**Admin-controlled overrides (via App Settings):**
| Key | Description |
|---|---|
| `OPENROUTER_API_KEY` | Override env var API key |
| `OPENROUTER_MODEL` | Override default AI model |
| `AI_ENABLED` | `true`/`false` — disable AI features |
| `AI_MAX_REQUESTS_PER_DAY` | Override daily limit |

---

## Project Structure

```
├── ats_builder/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/         # Auth, User model, AppSettings
│   ├── resume/           # Resume builder, PDF generation
│   ├── ats/              # ATS scoring engine
│   ├── ai_assistant/     # OpenRouter integration, chat
│   └── drive/            # Google Drive service
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── vercel.json
├── requirements.txt
├── manage.py
└── .env.example
```

---

## Security

- API keys managed via environment variables / admin settings — never exposed to frontend
- CSRF protection on all POST endpoints
- Per-user data isolation enforced at ORM level (all queries filtered by `user=request.user`)
- Session cookies set to `Secure` in production
- Rate limiting on AI endpoints (configurable per-user daily limit)
- XSS protection via Django template auto-escaping
