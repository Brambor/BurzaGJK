from django import forms

from .models import Offer, User, Book

class MakeOfferForm(forms.ModelForm):
	class Meta:
		model = Offer
		exclude = ['active', 'vendor', 'buyer']
		widgets = {
			'will_be_active': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
		}

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		password = forms.CharField(widget=forms.PasswordInput)
		widgets = {
			'password': forms.PasswordInput(),
		}

class AddBookForm(forms.ModelForm):
	class Meta:
		model = Book
		exclude = ['ISBN', 'subject']
