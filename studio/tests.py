from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .content import DECORATIVE_BORDER_CHOICES
from .models import Capability, Inquiry, ProcessStep, Project, ServiceOffering, SiteSettings


class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            "service": "web", "summary": "A community website.",
            "cover": "projects/covers/example.jpg", "cover_alt": "Website home screen",
            "challenge": "Connect members.", "approach": "Build a directory.",
        }
        cls.live = Project.objects.create(title="Published project", slug="published", published=True, featured=True, **data)
        cls.draft = Project.objects.create(title="Private draft", slug="draft", featured=True, **data)
        cls.other = Project.objects.create(title="Photography project", slug="photography", published=True, **{**data, "service": "photo"})

    def test_home_features_only_published_featured_projects(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, self.live.title)
        self.assertNotContains(response, self.draft.title)
        self.assertNotContains(response, self.other.title)

    def test_drafts_are_not_publicly_accessible(self):
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(self.live.get_absolute_url()).status_code, 200)

    def test_filter_returns_only_requested_discipline(self):
        response = self.client.get(reverse("work"), {"service": "photo"}, HTTP_HX_REQUEST="true")
        self.assertContains(response, self.other.title)
        self.assertNotContains(response, self.live.title)
        self.assertNotContains(response, "<!doctype html>")

    def test_filter_url_is_a_complete_page_without_htmx(self):
        response = self.client.get(reverse("work"), {"service": "photo"})
        self.assertContains(response, "<!doctype html>")
        self.assertContains(response, self.other.title)

    def test_history_restore_returns_complete_page(self):
        response = self.client.get(reverse("work"), HTTP_HX_REQUEST="true", HTTP_HX_HISTORY_RESTORE_REQUEST="true")
        self.assertContains(response, "<!doctype html>")

    def test_home_uses_optimized_initial_assets(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "studio-founder.webp")
        self.assertContains(response, 'loading="lazy"')
        self.assertNotContains(response, "vendor/gsap/gsap.min.js")


class InquiryTests(TestCase):
    def setUp(self):
        self.data = {"name": "Amina", "email": "amina@example.com", "organization": "Community", "service": "community", "message": "We would like a member platform."}

    def test_htmx_submission_is_saved(self):
        response = self.client.post(reverse("contact"), self.data, HTTP_HX_REQUEST="true")
        self.assertContains(response, "And so it begins.")
        self.assertEqual(Inquiry.objects.get().email, self.data["email"])

    def test_invalid_submission_retains_values_and_does_not_save(self):
        response = self.client.post(reverse("contact"), {**self.data, "email": "invalid"}, HTTP_HX_REQUEST="true")
        self.assertContains(response, "Enter a valid email address")
        self.assertContains(response, self.data["message"])
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_honeypot_rejects_submission(self):
        self.client.post(reverse("contact"), {**self.data, "website": "https://spam.example"})
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_standard_form_redirect_prevents_refresh_resubmission(self):
        response = self.client.post(reverse("contact"), self.data)
        self.assertRedirects(response, reverse("contact_success"))
        self.assertEqual(Inquiry.objects.count(), 1)

    def test_csrf_is_enforced(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("contact"), self.data, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 403)


class AdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="editor", email="editor@example.com", password="safe-password"
        )

    def test_site_settings_is_a_singleton(self):
        self.assertEqual(SiteSettings.objects.count(), 1)
        settings = SiteSettings.objects.get()
        settings.pk = 9
        settings.save()
        self.assertEqual(settings.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_admin_displays_site_settings(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Site settings")

    def test_site_settings_admin_includes_a_palette_preview(self):
        self.client.force_login(self.user)
        settings = SiteSettings.objects.get()
        response = self.client.get(reverse("admin:studio_sitesettings_change", args=[settings.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Palette preview")
        self.assertContains(response, "Decorative border")

    def test_selected_decorative_border_is_applied_to_public_site(self):
        settings = SiteSettings.objects.get()
        settings.decorative_border = "brackets"
        settings.save()
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'data-border-style="brackets"')

    def test_admin_offers_fifteen_decorative_borders_including_floral(self):
        self.assertEqual(len(DECORATIVE_BORDER_CHOICES), 15)
        self.assertIn(("floral", "Floral corner frame"), DECORATIVE_BORDER_CHOICES)

    def test_selected_palette_is_exposed_to_the_public_theme(self):
        settings = SiteSettings.objects.get()
        settings.theme_palette = "coastline"
        settings.save()
        response = self.client.get(reverse("home"))
        self.assertContains(response, "--orange: #e66f55")
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_kenya_palette_is_exposed_to_the_public_theme(self):
        settings = SiteSettings.objects.get()
        settings.theme_palette = "kenya"
        settings.save()
        response = self.client.get(reverse("home"))
        self.assertContains(response, "--orange: #bb2328")
        self.assertContains(response, "--black: #111413")
        self.assertContains(response, "--tan: #f7f7f4")
        self.assertContains(response, "--yellow: #0a7037")
        self.assertContains(response, "--arrow: #ffffff")
        self.assertContains(response, 'data-theme="kenya"')
        self.assertContains(response, 'stroke="#ffffff"')
        self.assertNotContains(response, 'stroke="#ef642d"')

    def test_custom_site_settings_rendered_on_home(self):
        settings = SiteSettings.objects.get()
        settings.welcome_heading = "CUSTOM STUDIO HEADLINE"
        settings.what_we_do_title = "Custom What We Do"
        settings.about_heading = "Custom About Heading"
        settings.save()
        response = self.client.get(reverse("home"))
        self.assertContains(response, "CUSTOM STUDIO HEADLINE")
        self.assertContains(response, "Custom What We Do")
        self.assertContains(response, "Custom About Heading")

    def test_dynamic_process_steps_rendered_on_home(self):
        ProcessStep.objects.all().delete()
        ProcessStep.objects.create(step_number="10", title="Custom Audit Step", description="Detailed audit test", sort_order=1)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Custom Audit Step")
        self.assertContains(response, "Detailed audit test")

    def test_dynamic_capabilities_rendered_on_home(self):
        Capability.objects.all().delete()
        Capability.objects.create(number="7", title="Custom AI Strategy", description="AI roadmap planning", sort_order=1)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Custom AI Strategy")
        self.assertContains(response, "AI roadmap planning")

    def test_dynamic_services_rendered_on_home(self):
        ServiceOffering.objects.all().delete()
        ServiceOffering.objects.create(
            key="custom-service",
            name="Brand Consulting",
            summary_line="Precision advisory.",
            description="High impact brand leadership.",
            modal_description="Comprehensive quarterly strategy.",
            published=True,
            sort_order=1,
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Brand Consulting")
        self.assertContains(response, "Comprehensive quarterly strategy.")

    def test_admin_can_access_new_model_changelists(self):
        self.client.force_login(self.user)
        for url_name in [
            "admin:studio_processstep_changelist",
            "admin:studio_capability_changelist",
            "admin:studio_serviceoffering_changelist",
        ]:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
