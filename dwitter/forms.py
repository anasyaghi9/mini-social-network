from django import forms
from .models import Dweet


class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "textarea",
            "placeholder": "Dweet something...",
            "rows": 8,
        }),
        label="",
    )

    class Meta:
        model = Dweet
        exclude = ("user", )