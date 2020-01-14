from Intent import views
from django.conf.urls import url
from audio.views import (
    upload_photo
    )

urlpatterns = [
       url(r'^upload/$', upload_photo)
]
