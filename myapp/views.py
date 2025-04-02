

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PositionDetail  # import model


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