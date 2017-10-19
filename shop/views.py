from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from .models import Offer


def offer_list(request):
	context = {"offers": Offer.objects.all()}

	template = loader.get_template('grid_of_offers.html')
	return HttpResponse(template.render(context, request))

def offer_detail(request, offer):
	context = {"offer": get_object_or_404(Offer, id=offer)}

	template = loader.get_template('offer_detail.html')
	return HttpResponse(template.render(context, request))
