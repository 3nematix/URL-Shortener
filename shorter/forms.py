from django.forms import ModelForm
from .models import Link


class UrlForm(ModelForm):
    class Meta:
        model = Link
        fields = ['full_url', 'key']
        labels = {
            'full_url': 'Insert your URL'
        }
        help_texts = {
            'full_url': '👤&nbsp; To use it just easily paste your URL address above.',
            'key': '🔑&nbsp; The maximum length of a Protection Key is 32 characters.'
        }
