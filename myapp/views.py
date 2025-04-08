

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import PositionDetail  # import model
from .models import AccidentNode
from geopy.distance import geodesic

@api_view(['GET'])
def get_nearby_accidents(request):
    # Obtain coordinates and range from front end (in kilometers)
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))
    radius = float(request.GET.get('radius', 1))

    # Get all data (required fields only)
    accidents = AccidentNode.objects.values(
        'accident_no', 'node_type', 'lga_name', 'latitude', 'longitude'
    )

    # Filtering nearby data
    nearby_data = []
    target_coord = (lat, lng)
    for accident in accidents:
        accident_coord = (accident['latitude'], accident['longitude'])
        distance = geodesic(target_coord, accident_coord).kilometers
        if distance <= radius:
            accident['distance'] = round(distance, 2)  # Add distance field
            nearby_data.append(accident)

    return JsonResponse({'data': nearby_data})


@api_view(['GET'])
def test_uv_connectivity(request):
    try:
        # Avoid ORM Interference Completely with RAW SQL Queries
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT year, month, lat, lon, avg_uv_index FROM processed_avg_monthly_uv LIMIT 1")
            row = cursor.fetchone()

        if row:
            return Response({
                "status": "success",
                "data": {
                    "year": row[0],
                    "month": row[1],
                    "lat": row[2],
                    "lon": row[3],
                    "avg_uv_index": row[4]
                }
            })
        return Response({"status": "empty"})
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Database error: {str(e)}"
        }, status=500)

@api_view(['GET'])
def api_example(request):
    try:
        # Querying the first row using ORM
        position = PositionDetail.objects.first()

        if position:
            data = {
                "id": position.id,
                "latitude": position.latitude,
                "longitude": position.longitude,
                "timestamp": position.timestamp
            }
            return Response(data)
        else:
            return Response({"error": "No data found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)