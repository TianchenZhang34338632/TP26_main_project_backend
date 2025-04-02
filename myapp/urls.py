from django.urls import path
from . import views

urlpatterns = [
    path('api/example/', views.api_example, name='api-example'),
    path('api/test-uv-connectivity/', views.test_uv_connectivity, name='test-uv-connectivity'),
]