from django.db import migrations


def seed_data(apps, schema_editor):
    SiteSettings = apps.get_model("studio", "SiteSettings")
    ProcessStep = apps.get_model("studio", "ProcessStep")
    Capability = apps.get_model("studio", "Capability")
    ServiceOffering = apps.get_model("studio", "ServiceOffering")

    # Seed or update SiteSettings defaults
    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    if not settings.what_we_do_body:
        settings.what_we_do_body = (
            "I transform brands into powerful assets. I do this by uncovering the unique value "
            "present in your business and translating it into a brand identity that truly reflects your vision.\n\n"
            "Whether you're evolving an existing brand or starting fresh, I'm here to capture the essence "
            "of your business and communicate it powerfully.\n\n"
            "It's not just about logos or color schemes – it's about creating a brand that's authentically "
            "you, resonates with your audience, and drives your business forward."
        )
    if not settings.how_step1_body:
        settings.how_step1_body = (
            "The first step to working with sababisha is the sababisha.review. It's a deep-dive interview "
            "where we get to know everything about your practice — where you are, where you've been, and where "
            "you want to go. We'll help uncover the brand opportunities already waiting for you and pinpoint "
            "what to start and stop doing to own your space."
        )
    if not settings.how_step2_body:
        settings.how_step2_body = (
            "After your sababisha.review reveals what makes your business uniquely awesome, we bring that to life. "
            "Our brand transformation process turns those insights into strategy, messaging, and design that gets "
            "you noticed. Simple as that."
        )
    if not settings.about_body:
        settings.about_body = (
            "We built sababisha.africa on a simple belief: passionate businesses deserve powerful brands. "
            "With years of experience in design and strategy, we've seen firsthand how the right branding can "
            "transform a business. We're here to help you uncover the unique story that sets your business apart "
            "and turn it into a brand that truly resonates. Let's create something that's authentically you — "
            "and irresistible to your audience."
        )
    if not settings.whos_this_for_body:
        settings.whos_this_for_body = (
            "sababisha.africa is for business owners who are passionate about what they do. If you've been focusing "
            "on perfecting your product or service, and now realize your brand needs to catch up, we're here for you.\n\n"
            "Whether your current brand needs a refresh or you're starting from scratch, we'll help you build "
            "something that shows who you really are and where you're headed."
        )
    settings.save()

    # Seed Process steps
    process_data = [
        ("1", "vibe check", "A free 15-minute call to discuss your business and explore how we can elevate your brand.", 1),
        ("2", "sababisha.review", "A deep-dive interview to uncover your brand's potential and pinpoint opportunities.", 2),
        ("3", "Strategy Development", "We craft a unique brand strategy document based on our findings.", 3),
        ("4", "Design & Implementation", "We bring your brand to life across all touchpoints, ensuring consistency and impact.", 4),
        ("5", "Launch & Support", "We're with you as your new brand goes live, making sure everything lands exactly right.", 5),
    ]
    for num, title, desc, order in process_data:
        ProcessStep.objects.get_or_create(
            step_number=num,
            defaults={"title": title, "description": desc, "sort_order": order},
        )

    # Seed Capabilities
    capabilities_data = [
        ("1", "Brand Strategy", "We believe in creating a solid brand foundation. Together, we'll develop a plan that aligns your brand with your business goals and sets you apart in your market.", 1),
        ("2", "Visual Identity", "A strong visual identity can speak volumes. We're here to help you craft or refine the visual elements that make your brand uniquely you.", 2),
        ("3", "Messaging", "Your message matters. We'll work with you to find the right words that connect with your audience and showcase what makes your business special.", 3),
        ("4", "Web Design & Dev", "In today's digital world, your website is often the first impression. We're passionate about creating online spaces that represent your brand effectively.", 4),
        ("5", "Photography & Film", "Sometimes, a picture really is worth a thousand words. We're excited about the power of visual storytelling to bring your brand to life.", 5),
    ]
    for num, title, desc, order in capabilities_data:
        Capability.objects.get_or_create(
            number=num,
            defaults={"title": title, "description": desc, "sort_order": order},
        )

    # Seed Service Offerings
    services_data = [
        ("web-development", "Web Development", "Web", "Built to do more.", "Purpose-built websites that are fast, accessible, easy to manage, and designed to turn attention into action.", "Purpose-built websites that are fast, accessible, easy to manage, and designed to turn attention into action.", "Websites / E-commerce / Web apps", 1),
        ("branding", "Branding", "Brand", "A clear brand foundation.", "A clear brand foundation: strategy, positioning, visual identity, and the practical tools to use it with confidence.", "A clear brand foundation: strategy, positioning, visual identity, and the practical tools to use it with confidence.", "Brand identity / Strategy / Guidelines", 2),
        ("graphic-design", "Graphic Design", "Design", "Impossible to ignore.", "Distinct campaign, editorial, social, and print design that makes every brand touchpoint feel considered and connected.", "Distinct campaign, editorial, social, and print design that makes every brand touchpoint feel considered and connected.", "Brand identity / Digital / Print", 3),
        ("videography", "Videography", "Film", "Make them feel something.", "Concept, direction, filming, and edits that give your brand a moving story people want to keep watching.", "Concept, direction, filming, and edits that give your brand a moving story people want to keep watching.", "Brand films / Events / Social content", 4),
        ("photography", "Photography", "Photo", "A different point of view.", "Original imagery for your people, products, spaces, and campaigns—planned around the way your audience sees your business.", "Original imagery for your people, products, spaces, and campaigns—planned around the way your audience sees your business.", "Portraits / Products / Events", 5),
        ("digital-storytelling", "Digital Storytelling", "Story", "Connect across channels.", "A connected narrative across words, visuals, and digital channels that makes your value instantly easier to understand.", "A connected narrative across words, visuals, and digital channels that makes your value instantly easier to understand.", "Copywriting / Narrative / Content", 6),
        ("service-portals", "Service Portals", "Portals", "Streamline member interactions.", "Focused online portals that make it easier for customers, teams, or partners to find information and complete important tasks.", "Focused online portals that make it easier for customers, teams, or partners to find information and complete important tasks.", "Portals / Dashboards / Self-service", 7),
        ("service-systems", "Service Systems", "Systems", "Less friction. More flow.", "Thoughtful internal systems and workflows that reduce friction, create consistency, and help your service scale.", "Thoughtful internal systems and workflows that reduce friction, create consistency, and help your service scale.", "Workflows / Internal tools / Automations", 8),
        ("communication-strategy", "Communication Strategy", "Comms", "Clarity with purpose.", "A practical plan for what to say, who to say it to, and how each message supports your wider business goals.", "A practical plan for what to say, who to say it to, and how each message supports your wider business goals.", "Messaging / Campaigns / Positioning", 9),
    ]
    for key, name, short, line, desc, modal_desc, tags, order in services_data:
        ServiceOffering.objects.get_or_create(
            key=key,
            defaults={
                "name": name,
                "short_name": short,
                "summary_line": line,
                "description": desc,
                "modal_description": modal_desc,
                "tags": tags,
                "sort_order": order,
                "published": True,
            },
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("studio", "0005_capability_processstep_serviceoffering_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=noop),
    ]
