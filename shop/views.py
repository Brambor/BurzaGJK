from django.http import HttpResponse
from django.template import loader
from .models import Offer


def index_view(request):
	context = {"offers": Offer.objects.all(),
				"off:": Offer.objects.all()[0],
	}
	print(context["offers"][0].get_img())
	template = loader.get_template('index.html')
	return HttpResponse(template.render(context, request))
