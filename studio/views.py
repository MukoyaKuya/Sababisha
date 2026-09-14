from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .content import SERVICES
from .forms import InquiryForm
from .models import Capability, ProcessStep, Project, ServiceOffering


def get_services():
    offerings = ServiceOffering.objects.filter(published=True)
    if offerings.exists():
        return [
            {
                "key": s.key,
                "number": f"0{idx+1}"[-2:],
                "name": s.name,
                "short": s.short_name or s.name,
                "line": s.summary_line,
                "description": s.description,
                "modal_description": s.modal_description or s.description,
                "tags": s.tags,
                "icon_image": s.icon_image,
                "icon_svg": s.icon_svg,
            }
            for idx, s in enumerate(offerings)
        ]
    return SERVICES


@require_GET
def home(request):
    services = get_services()
    return render(request, "studio/home.html", {
        "services": services,
        "process_steps": ProcessStep.objects.all(),
        "capabilities": Capability.objects.all(),
        "projects": Project.objects.filter(published=True, featured=True)[:4],
        "form": InquiryForm(),
    })


@require_GET
def work(request):
    service = request.GET.get("service", "")
    projects = Project.objects.filter(published=True)
    if service in dict((item["key"], item["name"]) for item in SERVICES):
        projects = projects.filter(service=service)
    else:
        service = ""
    partial = request.headers.get("HX-Request") == "true" and request.headers.get("HX-History-Restore-Request") != "true"
    template = "studio/partials/project_grid.html" if partial else "studio/work.html"
    return render(request, template, {"projects": projects, "services": SERVICES, "selected": service})


@require_GET
def project(request, slug):
    return render(request, "studio/project.html", {
        "project": get_object_or_404(Project.objects.prefetch_related("images"), slug=slug, published=True),
    })


@require_http_methods(["GET", "POST"])
def contact(request):
    form = InquiryForm(request.POST or None)
    sent = False
    if request.method == "POST" and form.is_valid():
        form.save()
        sent = True
        if request.headers.get("HX-Request") != "true":
            return redirect("contact_success")
    template = "studio/partials/inquiry.html" if request.headers.get("HX-Request") == "true" else "studio/contact.html"
    return render(request, template, {"form": form, "sent": sent})


@require_GET
def contact_success(request):
    return render(request, "studio/contact.html", {"sent": True})
