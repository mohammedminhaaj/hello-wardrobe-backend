from django.urls import path
from . import views

urlpatterns = [
    path('get-state/', views.load_initial_state, name='state'),
]