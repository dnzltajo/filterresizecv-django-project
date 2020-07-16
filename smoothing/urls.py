from django.urls import path
from .views import Home, loading

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('Output', loading, name='loading'),
]