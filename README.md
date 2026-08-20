# ATS Resume Builder

A production-ready **ATS Resume Builder + ATS Score Checker + AI Career Assistant** built with Django, HTML5, CSS3, vanilla JavaScript, and SQLite/PostgreSQL. Designed for **Vercel deployment**.

## Features

- **Resume Builder** — Classic 1-column ATS-friendly template, live preview, PDF export
- **ATS Score Checker** — Keyword matching, section analysis, formatting checks, recommendations
- **AI Career Assistant** — Powered by OpenRouter; improve bullet points, generate summaries, tailor resumes
- **Google Drive Integration** — Store resumes in your own Google Drive folder
- **Dual Auth** — Google OAuth + email/password login
- **Dark/Light Mode** — System preference auto-detected, manual toggle
- **Floating AI Chat Widget** — Available on every page + dedicated AI page
- **Admin Panel** — Full Django admin for users, templates, ATS config, AI settings

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
   - Production: `https://yourdomain.vercel.app/accounts/google/login/callback/`
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
1. Go to [vercel.com](https://vercel.com) → New Project → Import your GitHub repo
2. **Framework Preset**: Other
3. **Build Command**: `bash build_files.sh`
4. **Output Directory**: `staticfiles`
5. Add all environment variables from `.env.example` in Vercel Project Settings → Environment Variables
6. Deploy!

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
