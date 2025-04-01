from django.urls import path
from . import views

urlpatterns = [
    path('api/example/', views.api_example, name='api-example'),
]