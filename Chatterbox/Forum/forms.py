from django import forms
from .models import Ads

class AdForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['title', 'description', 'category']
    description = forms.CharField(widget=forms.Textarea, required=True)