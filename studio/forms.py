from django import forms
from .models import Appointment, AvailabilityDay, Inquiry, ServiceOffering


class InquiryForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Inquiry
        fields = ["name", "email", "organization", "service", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com", "autocomplete": "email"}),
            "organization": forms.TextInput(attrs={"placeholder": "Company or community (optional)", "autocomplete": "organization"}),
            "message": forms.Textarea(attrs={"placeholder": "The idea, the challenge, the big ambition…", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"] = forms.ChoiceField(
            choices=[("", "What are you looking for?")]
            + [(service.key, service.name) for service in ServiceOffering.objects.filter(published=True)],
        )

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Please leave this field empty.")
        return ""


class AppointmentForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    selected_date = forms.DateField(required=True, input_formats=["%Y-%m-%d"], widget=forms.HiddenInput)

    class Meta:
        model = Appointment
        fields = ["name", "email", "organization", "service", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].choices = [("", "What are you looking for?")] + [
            (service.key, service.name) for service in ServiceOffering.objects.filter(published=True)
        ]

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Please leave this field empty.")
        return ""

    def clean_selected_date(self):
        selected_date = self.cleaned_data["selected_date"]
        try:
            day = AvailabilityDay.objects.get(date=selected_date, available=True)
        except AvailabilityDay.DoesNotExist as error:
            raise forms.ValidationError("That date is no longer available. Please choose another.") from error
        if hasattr(day, "appointment"):
            raise forms.ValidationError("That date has just been requested. Please choose another.")
        self.availability_day = day
        return selected_date

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.availability_day = self.availability_day
        if commit:
            appointment.save()
        return appointment
