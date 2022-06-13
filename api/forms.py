
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SingUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']
        Widgets={ 'username':forms.TextInput(attrs={'class':'form-control'}),
                    'first_name':forms.TextInput(attrs={'class':'form-control'}),
                    'last_name':forms.TextInput(attrs={'class':'form-control'}),
                    'email':forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

        }
        