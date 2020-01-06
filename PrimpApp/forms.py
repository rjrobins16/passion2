from django import forms
from django.forms import ModelForm
from .models import AllUser
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

# all users main account sign up
class NewUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = User
        labels = {
                "email": "Email "
            }
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        help_texts = {
                            'username': None,
                            'email': None,
                        }

# main user log in for all users

class SignInForm(ModelForm):

     password = forms.CharField(widget=forms.PasswordInput)
     class Meta:
             model = User
             fields = ['username', 'password']
             help_texts = {
                                         'username': None,
                                     }


#intial profile completion, AllUsers form

class AllUsersForm(ModelForm):
    class Meta:

        widgets = {'DateOfBirth': DateInput(),
                    'AccountType': forms.HiddenInput(),
                    'BusinessName':forms.HiddenInput(),
                    'user':forms.HiddenInput(),
                    'lat': forms.HiddenInput(),
                    'lng':forms.HiddenInput(),
                    'TypeofStylist':forms.HiddenInput()}
        model = AllUser
        labels = {
                        "DateOfBirth": "Date of Birth "
                    }
        fields = '__all__'

