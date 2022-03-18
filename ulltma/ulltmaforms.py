from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignInForm(forms.Form):
	firstname = forms.CharField(label = '', max_length=100, widget=forms.TextInput(attrs = {'class' : 'formbox'}))
	lastname = forms.CharField(label = '', max_length=100, widget=forms.TextInput(attrs = {'class' : 'formbox'}))
	email = forms.CharField(label = '', max_length=100, widget=forms.TextInput(attrs = {'class' : 'formbox'}))
	pword = forms.CharField(label = '', max_length=100, widget=forms.PasswordInput(attrs = {'class' : 'formbox'}))
	pconfirm = forms.CharField(label = '', max_length=100, widget=forms.PasswordInput(attrs = {'class' : 'formbox'}))


class ChangePWordForm(forms.Form):
	pword = forms.CharField(label = '', max_length=100, widget=forms.PasswordInput(attrs = {'class' : 'formbox'}))
	pconfirm = forms.CharField(label = '', max_length=100, widget=forms.PasswordInput(attrs = {'class' : 'formbox'}))


class ChangePWordLoginForm(forms.Form):
	email = forms.CharField(label = '', max_length=150)
	pword = forms.CharField(label = '', max_length=100, widget=forms.PasswordInput(attrs = {'class' : 'formbox'}))
	pconfirm = forms.CharField(label = '', max_length=100, widget=forms.PasswordInput(attrs = {'class' : 'formbox'}))

