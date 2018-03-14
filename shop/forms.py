from django import forms

from .models import Offer, User

class MakeOfferForm(forms.ModelForm):
	class Meta:
		model = Offer
		exclude = ['active', 'vendor', 'buyer']

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		password = forms.CharField(widget=forms.PasswordInput)
		widgets = {
			'password': forms.PasswordInput(),
		}
