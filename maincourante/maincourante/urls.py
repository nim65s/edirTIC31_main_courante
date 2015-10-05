from django.conf.urls import include, url

from tastypie.api import Api

from .api import MessageResource
from .views import MainView

v1_api = Api(api_name='v1')
v1_api.register(MessageResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', MainView.as_view(), name='main'),
]
