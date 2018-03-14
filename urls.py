"""BurzaGJK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from shop.views import *

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^general', general_list, name='general_filter'),
	url(r'^clusters/all$', cluster_list, name='clusters_all'),
	url(r'^offers/(?P<offer>[0-9]+)', offer_detail, name='offer_detail'),
	url(r'^process_sell', process_sell, name='process_sell'),
	url(r'^process_buy', process_buy, name='process_buy'),
	url(r'^login$', login_view, name='login'),
	url(r'^logout$', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
