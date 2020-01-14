from django import forms
from django_mysql.forms import SimpleListField

class IntentForm(forms.Form):
    intent_data = forms.CharField(label='Intent Data', max_length=250)
    training_phrases =  SimpleListField(forms.CharField())
    responses = forms.CharField(label='Responses', max_length=250)
    