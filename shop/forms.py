from django.forms import ModelForm

from .models import Offer, User

class MakeOfferForm(ModelForm):
	class Meta:
		model = Offer
		exclude = ["active", "vendor", "buyer"]
