# Velcoris Industries — Digital Infrastructure & Backend-IT Fellowship Assignment

A working assessment prototype for the two tasks in the Velcoris Industries Round 1 brief: a responsive corporate website redesign and an enquiry-management backend.

## What is included

- Responsive industrial-materials website (HTML/CSS/JavaScript served by Flask).
- Contact/enquiry form with client-side and server-side validation.
- Flask REST endpoint `POST /api/enquiries`.
- SQLite persistence using parameterised SQL.
- Session-protected admin login at `/admin/login`.
- Admin dashboard at `/admin` to review enquiries and update status.
- Health endpoint at `/health`.
- Security headers, honeypot anti-bot field, input length limits and safe output escaping through Jinja templates.
- Assignment analysis and implementation roadmap in `docs/`.

## Requirements

- Python 3.10+
- pip

## Run locally (Windows PowerShell)

```powershell
# 1. Activate your virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# 2. Install requirements (including Flask and python-dotenv)
pip install -r requirements.txt

# 3. Environment configuration is automatically loaded from `.env` via python-dotenv:
#    SECRET_KEY=1a71745918d743e3a7a2e59d57bf56fdd0ccb94947fc1cfadef1e544ba18f730
#    ADMIN_USERNAME=admin
#    ADMIN_PASSWORD=admin123
#    DATABASE_PATH=instance/velcoris.db

# 4. Start the server
python run.py
```

Open `http://127.0.0.1:5000`.

Admin portal: `http://127.0.0.1:5000/admin/login` (Username: `admin`, Password: `admin123` as configured in `.env`).

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

The database connection is managed via `python-dotenv` reading `DATABASE_PATH` from `.env` (defaults to `instance/velcoris.db`).

## Accessing and Viewing Stored Queries

The assignment requires demonstrating how the stored queries can be accessed and viewed:

1. **Web Admin Dashboard (GUI)**:
   - Go to `http://127.0.0.1:5000/admin/login`
   - Sign in with credentials from `.env` (`admin` / `admin123`)
   - View the full table of submitted queries, metadata, statuses, and change inquiry status (`New`, `In Progress`, `Responded`, `Closed`).

2. **Command Line / Standalone Script**:
   - Run `python view_enquiries.py` in your terminal to directly inspect and dump stored queries from the SQLite database.
   - Or run `flask --app run.py view-enquiries`.

## Deploying to Vercel

The application is fully pre-configured for Vercel Serverless deployment with `vercel.json` and `api/index.py`:

### Option 1: Via Vercel CLI
```bash
npm i -g vercel
vercel
```

### Option 2: Via GitHub / Vercel Dashboard
1. Push your repository to GitHub (or GitLab/Bitbucket).
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Import this repository.
4. Set Environment Variables in Project Settings:
   - `SECRET_KEY`: `your-secure-random-secret`
   - `ADMIN_USERNAME`: `admin`
   - `ADMIN_PASSWORD`: `your-admin-password`
5. Click **Deploy**. Vercel will build the Python serverless function automatically.
*(Note: On serverless functions, the writable disk is ephemeral at `/tmp/velcoris.db`. For persistent high-volume production data, connect to managed cloud PostgreSQL via Supabase or Neon).*

## Test the workflow

1. Open the homepage and submit the contact form with test data you control.
2. Confirm the success message appears.
3. Open `/admin/login` and sign in with the environment credentials.
4. Confirm the enquiry appears in the dashboard.
5. Change its status (for example, New → In Progress) and save.
6. Refresh the page and confirm the status persists.
7. Check `/health` returns `{"status":"ok",...}`.

## API contract

`POST /api/enquiries` accepts form-encoded data or JSON:

- `name` (2–100 chars)
- `email` (valid email, max 254 chars)
- `organisation` (optional, max 120 chars)
- `enquiry_type` (`Sample request`, `Technical consultation`, `Partnership`, `General enquiry`)
- `subject` (3–140 chars)
- `message` (10–3000 chars)
- `website` (hidden honeypot; must remain empty)

Success: HTTP 201 with a confirmation message. Validation errors: HTTP 400 with an `errors` object.

## Important security and deployment notes

This is an educational prototype, not a production-ready customer relationship management system. Before public deployment:

- Set a long, random `SECRET_KEY` and strong unique admin password through a secret manager/environment variables.
- Replace the single shared admin credential with individual accounts, password hashing, MFA, role-based permissions and audit logs.
- Add CSRF protection to browser-authenticated state-changing admin forms, login rate limiting, lockout/alerting and abuse controls (CAPTCHA or managed bot protection where justified).
- Enforce HTTPS, configure secure cookie flags, trusted hosts, backups, monitoring and retention/deletion policies.
- Use PostgreSQL for concurrent production workloads, managed backups and migrations.
- Add transactional email notifications through an approved provider; do not expose SMTP credentials in source code.
- Review privacy notices and applicable Indian data-protection requirements with qualified counsel before collecting real personal data.

The prototype intentionally does not send emails, does not collect sensitive personal data, and does not claim that any of its infrastructure is currently used by Velcoris Industries.

## Project structure

```text
velcoris_assignment/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── routes.py
│   ├── templates/       # homepage, login, admin dashboard
│   └── static/          # CSS and browser JavaScript
├── docs/
│   ├── assignment_report.md
│   ├── architecture.md
│   └── verification_checklist.md
├── tests/
├── run.py
├── requirements.txt
└── README.md
```

## Academic integrity / candidate ownership

AI assistance was used to scaffold and implement this prototype. The candidate should independently run it, inspect and modify the code, verify the claims in the analysis, and be able to explain the request lifecycle, database schema, validation, session protection and production limitations before submission. Do not claim work or testing that you have not personally verified.
