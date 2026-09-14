# Sababisha Africa

A Django agency website with a blue-accented editorial design, desktop horizontal scrolling, mobile vertical layouts, and an admin-managed portfolio.

## Stack

- Python 3.12+ / Django 6
- PostgreSQL 17 (Docker Compose configuration included)
- HTMX 2 for portfolio filtering and project inquiries
- Alpine.js 3 for the navigation and service accordions
- Tailwind CSS 4 compiled locally, with a custom design layer

JavaScript dependencies are served locally through Django static files. The current typefaces are requested from Google Fonts; self-host them before deploying to environments that prohibit third-party font requests.

## Local setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
npm ci
npm run build
Copy-Item .env.example .env
```

Set a unique `DJANGO_SECRET_KEY` in `.env`. Start Docker Desktop, then:

```powershell
docker compose up -d db
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Website: http://127.0.0.1:8000/
- Portfolio: http://127.0.0.1:8000/work/
- Admin: http://127.0.0.1:8000/admin/

PostgreSQL is the default database. If PostgreSQL isn't running and you just want a local preview, set `USE_SQLITE=True` in `.env`, then run migrations and create an admin user. SQLite and PostgreSQL have separate data; switching the setting does not transfer projects.

## Adding your projects

1. Sign in to the admin and open **Projects → Add project**.
2. Enter the title, slug, discipline, summary, year, and optional client name.
3. Upload a cover image and describe it in the alternative-text field.
4. Add the challenge, approach, and any real outcomes.
5. Add gallery images using the inline image fields.
6. Enable **Published** to show it in the portfolio.
7. Enable **Featured** to show it on the homepage (up to four projects).
8. Use **Sort order** to control presentation order; lower numbers appear first.

Draft projects are excluded from public lists and return 404 at their detail URL. No sample client claims or fake portfolio entries are included.

## Inquiries

The contact form validates and saves inquiries to **Admin → Inquiries**. Mark them as handled after following up. It works as an HTMX form and as a standard HTML POST. CSRF protection and a honeypot field are included. Email notifications are not configured; read inquiries in the admin.

## Frontend development

```powershell
npm run watch
```

- Layout and content: `templates/studio/home.html`
- Shared navigation: `templates/base.html`
- Service copy: `studio/content.py`
- Styling and Tailwind entry: `static/src/input.css`
- Scrolling, menu, and form behavior: `static/js/site.js`
- Compiled stylesheet: `static/css/site.css`

Desktop scrolling uses a sticky viewport and a transform driven by the native scroll position. It activates at widths of 992px+; smaller screens and browsers without JavaScript use a vertical page. The navigation supports direct section links, and keyboard focus brings off-screen panels into view.

## Verification

```powershell
python manage.py check
python manage.py test
npm run build
node --check static/js/site.js
```

Tests cover publication visibility, filters, HTMX history restoration, inquiry persistence, validation, CSRF, and the standard form fallback. To run these with SQLite for local verification only:

```powershell
$env:USE_SQLITE = 'True'
python manage.py test
```

## Deployment configuration

Set `DJANGO_DEBUG=False`, a unique secret, allowed hostnames, and PostgreSQL credentials. HTTPS redirects, secure cookies, and a one-year HSTS policy activate automatically outside debug mode. If TLS terminates at a trusted reverse proxy, set `TRUST_X_FORWARDED_PROTO=True`. Run migrations and `python manage.py collectstatic --noinput`. Serve the application through a production WSGI server, configure cache headers for static files and uploaded media, and back up the database and media uploads. The local Compose file provides the database only.
