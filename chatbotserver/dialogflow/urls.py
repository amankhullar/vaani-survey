from django.urls import path
from dialogflow import views
from django.conf.urls import url
from dialogflow.views import (
    home_view
    )

urlpatterns = [
    path('home/', home_view, name='home'),
    path('webhook/', views.webhook, name='webhook'),
]