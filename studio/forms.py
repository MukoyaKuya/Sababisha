from django import forms
from .models import Inquiry


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

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Please leave this field empty.")
        return ""
