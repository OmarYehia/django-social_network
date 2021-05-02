import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = forms.ChoiceField(widget=forms.RadioSelect(),choices=GENDER_CHOICES)
    date_of_birth = forms.DateField()


    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "gender", "date_of_birth")

        def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.gender = self.cleaned_data['gender']
            user.date_of_birth = self.cleaned_data['date_of_birth']
            if commit:
                user.save()

            return user

