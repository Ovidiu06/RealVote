from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('', views.ElectionEventsView.as_view(), name='dashboard'),
]