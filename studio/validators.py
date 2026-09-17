from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_cta_url(value):
    """Allow anchors, local paths, and explicit HTTPS destinations only."""
    if not value or value.startswith("#"):
        return
    if value.startswith("/") and not value.startswith("//"):
        return

    parsed = urlparse(value)
    if parsed.scheme == "https" and parsed.netloc:
        return
    raise ValidationError("Use an anchor, a site-relative path, or an HTTPS URL.")
