from django.forms import ModelForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'


class UserProfileForm(ModelForm):

    class Meta:
       widgets = {'DateOfBirth': DateInput(),
                   'is_stylist':forms.HiddenInput(),
                   'latitude':forms.HiddenInput(),
                   'longitude':forms.HiddenInput(),
                   'TypeofStylist':forms.HiddenInput()}
       model = Profile
       fields = ['DateOfBirth', 'Profile_Picture','is_stylist','latitude','longitude','TypeofStylist']


class NewUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        help_texts = {
                            'username': None,
                            'email': None,
                        }


class SignInForm(ModelForm):

     password = forms.CharField(widget=forms.PasswordInput)
     class Meta:
             model = User
             fields = ['username', 'password']

class StylistSignUp(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        help_texts = {
                    'username': None,
                    'email': None,
                }

