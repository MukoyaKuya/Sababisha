from django.db.utils import OperationalError, ProgrammingError

from .content import THEME_PALETTES


def site_theme(request):
    """Expose the selected, server-defined palette and site settings to public templates."""
    try:
        from .models import SiteSettings

        settings = SiteSettings.objects.first()
    except (OperationalError, ProgrammingError):
        settings = None

    palette_key = settings.theme_palette if settings else "embers"
    return {
        "active_palette_key": palette_key,
        "active_palette": THEME_PALETTES.get(palette_key, THEME_PALETTES["embers"]),
        "site_settings": settings,
    }

