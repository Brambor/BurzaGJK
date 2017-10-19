from django.http import HttpResponse
from django.template import loader
from .models import Offer


def list_offers(request):
	context = {"offers": Offer.objects.all()}

	template = loader.get_template('grid_of_offers.html')
	return HttpResponse(template.render(context, request))
