from django.contrib import admin
from django.utils.html import format_html, format_html_join
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from .models import (
    Capability,
    Inquiry,
    ProcessStep,
    Project,
    ProjectImage,
    ServiceOffering,
    SiteAsset,
    SiteContentBlock,
    SiteSettings,
)

admin.site.site_header = "Sababisha Africa / Studio"
admin.site.site_title = "Sababisha Admin"
admin.site.index_title = "Make things happen."


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ["title", "service", "year", "published", "featured", "sort_order"]
    list_filter = ["published", "featured", "service"]
    list_editable = ["published", "featured", "sort_order"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "client", "summary"]
    inlines = [ProjectImageInline]


@admin.register(Inquiry)
class InquiryAdmin(ModelAdmin):
    list_display = ["name", "email", "service", "created_at", "handled"]
    list_filter = ["handled", "service"]
    list_editable = ["handled"]
    readonly_fields = ["name", "email", "organization", "service", "message", "created_at"]
    search_fields = ["name", "email", "organization"]

    def has_add_permission(self, request):
        return False


@admin.register(ProcessStep)
class ProcessStepAdmin(ModelAdmin):
    list_display = ["step_number", "title", "sort_order"]
    list_editable = ["sort_order"]
    search_fields = ["title", "description"]


@admin.register(Capability)
class CapabilityAdmin(ModelAdmin):
    list_display = ["number", "title", "sort_order"]
    list_editable = ["sort_order"]
    search_fields = ["title", "description"]


@admin.register(ServiceOffering)
class ServiceOfferingAdmin(ModelAdmin):
    list_display = ["name", "key", "summary_line", "published", "sort_order"]
    list_filter = ["published"]
    list_editable = ["published", "sort_order"]
    search_fields = ["name", "description", "summary_line"]
    prepopulated_fields = {"key": ("name",)}
    fields = [
        "name",
        "key",
        "short_name",
        "summary_line",
        "description",
        "modal_description",
        "tags",
        "icon_image",
        "icon_svg",
        "sort_order",
        "published",
    ]


class SiteContentBlockInline(StackedInline):
    model = SiteContentBlock
    extra = 0
    fields = ["label", "key", "heading", "body", "action_label", "action_url", "image", "image_alt", "enabled", "sort_order"]
    ordering = ["sort_order", "label"]
    collapsible = True


class SiteAssetInline(TabularInline):
    model = SiteAsset
    extra = 0
    fields = ["label", "key", "image", "alt_text", "sort_order"]
    ordering = ["sort_order", "label"]
    collapsible = True


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    inlines = [SiteContentBlockInline, SiteAssetInline]
    fieldsets = (
        ("Brand Identity & SEO", {
            "fields": ("site_name", "site_tagline", "site_description"),
            "description": "Core identity and the default description used by search engines and social previews.",
        }),
        ("Colours & decorative borders", {
            "fields": ("theme_palette", "palette_preview", "decorative_border"),
            "description": "Choose the public site's colour palette and panel frame. Changes take effect immediately upon saving.",
        }),
        ("Brand Media & Mascots (All Uploads)", {
            "fields": (
                "nav_logo",
                "hero_logo",
                "founder_photo",
                "bridging_warrior",
                "standing_warrior",
                "winged_lion",
                "panther_mascot",
                "footer_mascot",
            ),
            "description": "Upload custom images to replace default brand logos and mascots. If left blank, the site uses its built-in assets.",
        }),
        ("Section 1: Hero / Welcome", {
            "fields": (
                "welcome_heading",
                "welcome_cta_top_text",
                "welcome_cta_top_line",
                "welcome_cta_bottom_line",
                "welcome_cta_url",
            ),
            "description": "Edit the headline, intro note, and CTA box on the initial panel.",
        }),
        ("Section 3: What We Do", {
            "fields": (
                "what_we_do_title",
                "what_we_do_heading",
                "what_we_do_body",
                "what_we_do_cta_label",
                "what_we_do_cta_url",
            ),
            "description": "Edit the 'What I do' card title, heading, 3-paragraph body, and CTA button.",
        }),
        ("Section 4: How We Do It", {
            "fields": (
                "how_we_do_it_title",
                "how_step1_heading",
                "how_step1_body",
                "how_step2_heading",
                "how_step2_body",
                "how_cta_label",
                "how_cta_url",
            ),
            "description": "Edit 'First things First', 'Second things second', and the process CTA.",
        }),
        ("Section 5: Our Process", {
            "fields": (
                "process_section_title",
                "process_cta_label",
                "process_cta_url",
            ),
            "description": "Individual process step cards (1 to 5) can be added, reordered, and edited under 'Process steps' in the sidebar.",
        }),
        ("Section 6: Pricing & Services", {
            "fields": (
                "pricing_section_title",
                "pricing_intro",
                "pricing_footer_text",
                "pricing_cta_label",
                "pricing_cta_url",
            ),
            "description": "Individual service offerings can be added, reordered, and edited under 'Service offerings' in the sidebar.",
        }),
        ("Section 8: About ('Hey, we're Sababisha!')", {
            "fields": ("about_heading", "about_body"),
            "description": "Edit the black box about statement.",
        }),
        ("Section 9: Who's This For", {
            "fields": (
                "whos_this_for_title",
                "whos_this_for_heading",
                "whos_this_for_body",
                "whos_this_for_cta_top_line",
                "whos_this_for_cta_bottom_line",
                "whos_this_for_cta_url",
            ),
            "description": "Edit the 'Are you a good fit?' card and schedule CTA.",
        }),
        ("Section 10: Capabilities", {
            "fields": (
                "capabilities_section_title",
                "capabilities_footer_text",
                "capabilities_cta_label",
                "capabilities_cta_url",
            ),
            "description": "Individual capability cards can be added, reordered, and edited under 'Capabilities' in the sidebar.",
        }),
        ("Section 11: Contact ('Let's Vibe')", {
            "fields": (
                "contact_section_title",
                "contact_heading",
                "contact_subtitle",
                "contact_footer_note",
                "contact_email",
                "contact_phone",
                "address",
            ),
            "description": "Edit the contact headline, subtitle, direct email address, and note.",
        }),
        ("Section 12: Footer & Social Channels", {
            "fields": (
                "footer_tagline",
                "footer_subtagline",
                "footer_social_text",
                "linkedin_url",
                "instagram_url",
                "x_url",
                "footer_copyright",
            ),
            "description": "Edit footer taglines, social channel links, and studio copyright text.",
        }),
        ("Record Metadata", {"fields": ("updated_at",)}),
    )
    readonly_fields = ["palette_preview", "updated_at"]

    @admin.display(description="Palette preview")
    def palette_preview(self, obj):
        palette = obj.palette
        swatches = format_html_join(
            "",
            '<span style="display:inline-block;width:42px;height:42px;border-radius:999px;margin-right:8px;background:{};border:1px solid #888"></span>',
            ((palette[key],) for key in ("primary", "ink", "surface", "accent")),
        )
        return format_html("<div>{}</div><strong>{}</strong>", swatches, palette["name"])

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
