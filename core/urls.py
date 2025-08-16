from django.urls import path
from . import views

urlpatterns = [
    path('', views.meeting_summary, name='home'),
]