from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=100, required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Username','autofocus':'autofocus'}))
    password = forms.CharField(label="", max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))