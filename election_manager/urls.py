from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('', views.ElectionEventsView.as_view(), name='dashboard'),
    path('my_elections/', views.ElectionEventsView.as_view(), name='my_elections'),
    path('my_elections/add/', views.AddElectionView.as_view(), name='add_election'),
]