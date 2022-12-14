from django.urls import path
from . import views

urlpatterns = [
    path('cv/', views.cv),
    path('', views.landing),
]
