from helloworld import views
from django.conf.urls import url
from .views import (
    HelloWorld,
    )

urlpatterns = [
	url(r'^(?P<id>[\w-]+)/edit/$', HelloWorld.as_view()),
]
