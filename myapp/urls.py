from django.urls import path
from . import views

urlpatterns = [
    path('api/accidents/', views.get_nearby_accidents, name='accident-data'),
    path('api/example/', views.api_example, name='api-example'),
    path('api/test-uv-connectivity/', views.test_uv_connectivity, name='test-uv-connectivity'),
]