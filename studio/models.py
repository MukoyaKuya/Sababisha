from django.db import models
from django.urls import reverse

from .content import DECORATIVE_BORDER_CHOICES, THEME_PALETTES, THEME_PALETTE_CHOICES
from .validators import validate_cta_url


class Project(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    client = models.CharField(max_length=160, blank=True)
    service = models.CharField(max_length=60)
    summary = models.CharField(max_length=260)
    cover = models.ImageField(upload_to="projects/covers/")
    cover_alt = models.CharField(max_length=200, help_text="Describe the image for screen readers.")
    challenge = models.TextField()
    approach = models.TextField()
    outcome = models.TextField(blank=True)
    website = models.URLField(blank=True)
    year = models.PositiveSmallIntegerField(default=2026)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-year", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project", kwargs={"slug": self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    alt = models.CharField(max_length=200)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "pk"]


class Inquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    organization = models.CharField(max_length=160, blank=True)
    service = models.CharField(max_length=60)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "inquiries"

    def __str__(self):
        return f"{self.name} — {self.get_service_display()}"


class AvailabilityDay(models.Model):
    """A calendar date the studio has opened for a vibe-check appointment."""

    date = models.DateField(unique=True)
    available = models.BooleanField(default=True)
    note = models.CharField(max_length=160, blank=True, help_text="Optional internal note, e.g. morning only.")

    class Meta:
        ordering = ["date"]
        verbose_name = "available appointment day"
        verbose_name_plural = "available appointment days"

    def __str__(self):
        return self.date.strftime("%a, %d %b %Y")


class Appointment(models.Model):
    """A public vibe-check request against an admin-opened calendar day."""

    availability_day = models.OneToOneField(AvailabilityDay, on_delete=models.PROTECT, related_name="appointment")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    organization = models.CharField(max_length=160, blank=True)
    service = models.CharField(max_length=60, blank=True)
    message = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ["availability_day__date"]

    def __str__(self):
        return f"{self.availability_day.date:%d %b} — {self.name}"


class SiteSettings(models.Model):
    """The single, admin-managed source for studio-wide settings."""

    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    site_name = models.CharField(max_length=120, default="Sababisha Africa")
    site_tagline = models.CharField(max_length=220, blank=True)
    site_description = models.TextField(blank=True, help_text="Used for search and social sharing descriptions.")
    contact_email = models.EmailField(blank=True, default="hello@sababisha.africa")
    contact_phone = models.CharField(max_length=60, blank=True)
    address = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com")
    instagram_url = models.URLField(blank=True, default="https://instagram.com")
    x_url = models.URLField(blank=True, default="https://x.com", verbose_name="X / Twitter URL")
    theme_palette = models.CharField(
        max_length=20,
        choices=THEME_PALETTE_CHOICES,
        default="embers",
        help_text="Changes the public site's primary, ink, surface, and accent colours.",
    )
    decorative_border = models.CharField(
        max_length=20,
        choices=DECORATIVE_BORDER_CHOICES,
        default="classic",
        help_text="Changes the decorative frame used around homepage panels.",
    )

    # Brand Media & Imagery Uploads
    nav_logo = models.ImageField(upload_to="brand/", blank=True, help_text="Light logo shown in drawer navigation footer (fallback: sababisha-zebra-logo-light.png).")
    hero_logo = models.ImageField(upload_to="brand/", blank=True, help_text="Main zebra logo displayed in the welcome hero (fallback: sababisha-zebra-logo.png).")
    founder_photo = models.ImageField(upload_to="brand/", blank=True, help_text="Studio director cover portrait (fallback: studio-founder.jpg).")
    bridging_warrior = models.ImageField(upload_to="brand/", blank=True, help_text="Custom illustration for the warrior bridging What We Do and How We Do It (fallback: animated warrior canvas).")
    standing_warrior = models.ImageField(upload_to="brand/", blank=True, help_text="Standing warrior graphic on process timeline (fallback: warrior-standing-clean.png).")
    winged_lion = models.ImageField(upload_to="brand/", blank=True, help_text="Winged lion mascot in Who's This For section (fallback: winged-lion.png).")
    panther_mascot = models.ImageField(upload_to="brand/", blank=True, help_text="Winged panther mascot in Let's Vibe section (fallback: cougar.png).")
    footer_mascot = models.ImageField(upload_to="brand/", blank=True, help_text="Sababisha mascot artwork in footer (fallback: clean-up-your-brand.png).")

    # Section 1: Welcome / Hero
    welcome_heading = models.TextField(blank=True, default="INTENTIONAL\nBRANDING\nFOR\nPASSIONATE\nBUSINESSES.", help_text="Main headline on the hero panel.")
    welcome_cta_top_text = models.TextField(blank=True, default="I help elevate existing brands and create new ones from scratch. I do it because I believe your brand should work as hard as you do.")
    welcome_cta_top_line = models.CharField(max_length=120, blank=True, default="Start your brand journey.")
    welcome_cta_bottom_line = models.CharField(max_length=120, blank=True, default="Schedule a vibe check.")
    welcome_cta_url = models.CharField(max_length=200, blank=True, default="#lets-vibe", validators=[validate_cta_url])

    # Section 3: What We Do
    what_we_do_title = models.CharField(max_length=80, blank=True, default="What I do")
    what_we_do_heading = models.CharField(max_length=200, blank=True, default="SABABISHA.AFRICA IS A\nBRANDING AGENCY.")
    what_we_do_body = models.TextField(blank=True, help_text="Paragraphs of copy for What We Do.")
    what_we_do_cta_label = models.CharField(max_length=120, blank=True, default="See how we uncover your story.")
    what_we_do_cta_url = models.CharField(max_length=200, blank=True, default="#how-we-do-it", validators=[validate_cta_url])

    # Section 4: How We Do It
    how_we_do_it_title = models.CharField(max_length=80, blank=True, default="How I do it")
    how_step1_heading = models.CharField(max_length=120, blank=True, default="First things First")
    how_step1_body = models.TextField(blank=True)
    how_step2_heading = models.CharField(max_length=120, blank=True, default="Second things second")
    how_step2_body = models.TextField(blank=True)
    how_cta_label = models.CharField(max_length=120, blank=True, default="Learn about our process")
    how_cta_url = models.CharField(max_length=200, blank=True, default="#our-process", validators=[validate_cta_url])

    # Section 5: Our Process
    process_section_title = models.CharField(max_length=80, blank=True, default="My process")
    process_cta_label = models.CharField(max_length=120, blank=True, default="Book a sababisha.vibecheck")
    process_cta_url = models.CharField(max_length=200, blank=True, default="#lets-vibe", validators=[validate_cta_url])

    # Section 6: Pricing
    pricing_section_title = models.CharField(max_length=80, blank=True, default="Pricing")
    pricing_intro = models.TextField(blank=True, default="Choose a service to see what it includes. Every engagement is shaped around your goals, so pricing is quoted to fit the work.")
    pricing_footer_text = models.CharField(max_length=160, blank=True, default="Need a tailored scope?")
    pricing_cta_label = models.CharField(max_length=120, blank=True, default="Book your sababisha.vibecheck now")
    pricing_cta_url = models.CharField(max_length=200, blank=True, default="#lets-vibe", validators=[validate_cta_url])

    # Section 8: About
    about_heading = models.CharField(max_length=120, blank=True, default="Hey, we're Sababisha!")
    about_body = models.TextField(blank=True)

    # Section 9: Who's This For
    whos_this_for_title = models.CharField(max_length=80, blank=True, default="Who’s this for?")
    whos_this_for_heading = models.CharField(max_length=120, blank=True, default="Are you a good fit?")
    whos_this_for_body = models.TextField(blank=True)
    whos_this_for_cta_top_line = models.CharField(max_length=120, blank=True, default="Start your brand journey.")
    whos_this_for_cta_bottom_line = models.CharField(max_length=120, blank=True, default="Schedule a vibe check.")
    whos_this_for_cta_url = models.CharField(max_length=200, blank=True, default="#lets-vibe", validators=[validate_cta_url])

    # Section 10: Capabilities
    capabilities_section_title = models.CharField(max_length=80, blank=True, default="My capabilities")
    capabilities_footer_text = models.CharField(max_length=160, blank=True, default="Want to explore your options?")
    capabilities_cta_label = models.CharField(max_length=120, blank=True, default="Book a sababisha.vibecheck")
    capabilities_cta_url = models.CharField(max_length=200, blank=True, default="#lets-vibe", validators=[validate_cta_url])

    # Section 11: Contact / Let's Vibe
    contact_section_title = models.CharField(max_length=80, blank=True, default="Let’s vibe")
    contact_heading = models.CharField(max_length=120, blank=True, default="Drop us a line")
    contact_subtitle = models.CharField(max_length=200, blank=True, default="Ready to create something fresh? Let's chat.")
    contact_footer_note = models.CharField(max_length=200, blank=True, default="More of an email person? Hit us up at:")

    # Section 12: Footer
    footer_tagline = models.CharField(max_length=160, blank=True, default="MAKE THINGS HAPPEN.")
    footer_subtagline = models.CharField(max_length=200, blank=True, default="SABABISHA AFRICA — INTENTIONAL BRANDING")
    footer_social_text = models.CharField(max_length=120, blank=True, default="Where we hang out online")
    footer_copyright = models.CharField(max_length=200, blank=True, default="Sababisha Africa Studio · Nairobi, Kenya")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    @property
    def palette(self):
        return THEME_PALETTES.get(self.theme_palette, THEME_PALETTES["embers"])

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class ProcessStep(models.Model):
    """An individual step in the Our Process timeline."""

    step_number = models.CharField(max_length=10, default="1", help_text="Number or label, e.g. 1, 2, 3")
    title = models.CharField(max_length=120)
    description = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "step_number"]
        verbose_name = "process step"
        verbose_name_plural = "process steps"

    def __str__(self):
        return f"{self.step_number}. {self.title}"


class Capability(models.Model):
    """An individual studio capability card."""

    number = models.CharField(max_length=10, default="1", help_text="Number or label, e.g. 1, 2, 3")
    title = models.CharField(max_length=120)
    description = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "number"]
        verbose_name = "capability"
        verbose_name_plural = "capabilities"

    def __str__(self):
        return f"{self.number}. {self.title}"


class ServiceOffering(models.Model):
    """An offering listed on the Pricing & Capabilities grid and in the service detail modal."""

    key = models.SlugField(max_length=60, unique=True, help_text="Unique internal slug, e.g. web-development, branding.")
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=40, blank=True)
    summary_line = models.CharField(max_length=200, blank=True, help_text="Short punchy line, e.g. Built to do more.")
    description = models.TextField(help_text="Detailed description of the service.")
    modal_description = models.TextField(blank=True, help_text="Text shown inside the service detail popup modal.")
    tags = models.CharField(max_length=240, blank=True, help_text="Discipline tags, e.g. Websites / E-commerce / Web apps")
    icon_image = models.ImageField(upload_to="services/", blank=True, help_text="Optional custom icon image for the service card.")
    sort_order = models.PositiveSmallIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "service offering"
        verbose_name_plural = "service offerings"

    def __str__(self):
        return self.name


class SiteContentBlock(models.Model):
    """Editable page copy and its optional call-to-action or illustration."""

    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name="content_blocks")
    key = models.SlugField(max_length=80, help_text="Stable internal name, e.g. hero or process.")
    label = models.CharField(max_length=120, help_text="Editor-friendly section name.")
    heading = models.CharField(max_length=300, blank=True)
    body = models.TextField(blank=True)
    action_label = models.CharField(max_length=120, blank=True)
    action_url = models.CharField(max_length=240, blank=True, help_text="Use a relative path or anchor, e.g. #lets-vibe.")
    image = models.ImageField(upload_to="site-content/", blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    enabled = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "label"]
        verbose_name = "content block"
        verbose_name_plural = "content blocks"

    def __str__(self):
        return self.label


class SiteAsset(models.Model):
    """A labelled upload library for brand marks, illustrations, and imagery."""

    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name="assets")
    key = models.SlugField(max_length=80, help_text="Stable internal name, e.g. primary-logo or hero-photo.")
    label = models.CharField(max_length=120)
    image = models.ImageField(upload_to="site-assets/")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "label"]
        verbose_name = "brand asset"
        verbose_name_plural = "brand assets"

    def __str__(self):
        return self.label
