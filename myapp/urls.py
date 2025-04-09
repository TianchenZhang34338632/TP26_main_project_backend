from django.urls import path
from . import views

urlpatterns = [
    path('api/postcode-scores/', views.get_postcode_scores, name='postcode_scores'),
    path('api/accidents/', views.get_nearby_accidents, name='accident-data'),
    path('api/analyze-accidents/', views.analyze_accidents, name='analyze_accidents_data')
]