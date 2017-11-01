from django.forms import ModelForm

from .models import Offer

class MakeOfferForm(ModelForm):
	class Meta:
		model = Offer
		fields = ["book", "description", "will_be_active", "price"]
