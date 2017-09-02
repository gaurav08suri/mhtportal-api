"""mhtportal URL Configuration

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
from django.conf.urls import (url,
                            include)
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import (obtain_jwt_token,
                                        refresh_jwt_token,
                                        verify_jwt_token)
from base.views import MeView


schema_view = get_schema_view(title='Mht Portal APIs')

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^me/', MeView.as_view(), name="me"),
    url(r'^base/', include('base.urls', namespace='base')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^api-info/$', schema_view, name='api-info'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
