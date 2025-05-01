from django.urls import path
from . import views

urlpatterns = [
    path('api/postcode-scores/', views.get_postcode_scores, name='postcode_scores'),
    path('api/accidents/', views.get_nearby_accidents, name='accident-data'),
    path('api/analyze-accidents/', views.analyze_accidents, name='analyze_accidents_data'),
    path('api/analyze-location/', views.get_postcode_by_coordinate, name='get_postcode_by_coordinate'),
    path('api/get-uv-index/', views.get_uv_index_by_year),
    path('api/crime-scores/', views.get_crime_scores, name='crime_scores'),
    path('api/facilities/', views.facilities_by_postcode, name='facilities')
]