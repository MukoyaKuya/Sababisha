import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "local-development-only-sababisha-change-before-deployment")
if not DEBUG and (
    SECRET_KEY.startswith("local-development")
    or SECRET_KEY.startswith("replace-with-")
):
    raise ValueError("Set DJANGO_SECRET_KEY before deploying.")
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "studio",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "studio.context_processors.site_theme",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("POSTGRES_DB", "sababisha"),
    "USER": os.getenv("POSTGRES_USER", "sababisha"),
    "PASSWORD": os.getenv("POSTGRES_PASSWORD", "sababisha-local"),
    "HOST": os.getenv("POSTGRES_HOST", "localhost"),
    "PORT": os.getenv("POSTGRES_PORT", "5432"),
}}
if os.getenv("USE_SQLITE", "False").lower() == "true":
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ("vendor/alpine", BASE_DIR / "node_modules/alpinejs/dist"),
    ("vendor/htmx", BASE_DIR / "node_modules/htmx.org/dist"),
]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# These defaults are safe for HTTPS deployments while retaining a frictionless
# local development experience. A TLS-terminating proxy must set
# TRUST_X_FORWARDED_PROTO=True so Django can identify secure requests.
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", str(not DEBUG)).lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", str(not DEBUG)).lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", str(not DEBUG)).lower() == "true"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000" if not DEBUG else "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", str(not DEBUG)).lower() == "true"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "False").lower() == "true"
if os.getenv("TRUST_X_FORWARDED_PROTO", "False").lower() == "true":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from django.urls import reverse_lazy

# Unfold enhances Django's built-in admin without changing the public site.
UNFOLD = {
    "SITE_TITLE": "Sababisha Admin",
    "SITE_HEADER": "Sababisha Africa",
    "SITE_SUBHEADER": "Content Studio",
    "SITE_URL": "/",
    "SHOW_VIEW_ON_SITE": True,
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Editorial & Page Sections",
                "separator": True,
                "items": [
                    {
                        "title": "All Page Sections & Media",
                        "icon": "auto_stories",
                        "link": reverse_lazy("admin:studio_sitesettings_change", args=[1]),
                    },
                    {
                        "title": "Process Steps (1 to 5)",
                        "icon": "timeline",
                        "link": reverse_lazy("admin:studio_processstep_changelist"),
                    },
                    {
                        "title": "Capabilities (1 to 5)",
                        "icon": "auto_awesome",
                        "link": reverse_lazy("admin:studio_capability_changelist"),
                    },
                    {
                        "title": "Services & Pricing (1 to 9)",
                        "icon": "sell",
                        "link": reverse_lazy("admin:studio_serviceoffering_changelist"),
                    },
                ],
            },
            {
                "title": "Portfolio & Leads",
                "separator": True,
                "items": [
                    {
                        "title": "Projects",
                        "icon": "collections",
                        "link": reverse_lazy("admin:studio_project_changelist"),
                    },
                    {
                        "title": "Inquiries",
                        "icon": "mail",
                        "link": reverse_lazy("admin:studio_inquiry_changelist"),
                    },
                ],
            },
            {
                "title": "Authentication",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}

