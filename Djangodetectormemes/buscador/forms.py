from django.contrib.auth.forms import *


CHOICES =(
    ("todas", "Todas"),
    ("instagram", "Instagram"),
    ("twitter", "Twitter"),
    ("reddit", "Reddit"),
    ("telegram", "Telegram")
)

class searchDataForm(forms.Form):

    keyword = forms.CharField(max_length=100, label='Keyword')
    source = forms.ChoiceField(choices=CHOICES, label ='sources')
