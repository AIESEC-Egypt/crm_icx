from django import forms
from django.contrib.auth.forms import UserCreationForm

from crm_icx.core.models import Committee
from .models import User


class CustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    expa_id = forms.CharField(max_length=6, label='Expa ID')

    committee = forms.ModelChoiceField(queryset=Committee.objects.filter(parent_committee__id=1609))

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'expa_id',)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.expa_id = self.cleaned_data['expa_id']
        user.committee = self.cleaned_data['committee']
        user.save()

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
