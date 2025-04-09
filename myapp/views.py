

from rest_framework.decorators import api_view
from .models import AccidentNode
from geopy.distance import geodesic
from .models import VicPostcodeScore
from django.http import JsonResponse
from django.db import connection
from math import radians, cos, sin, asin, sqrt
import pandas as pd


def haversine(lat1, lon1, lat2, lon2):
    """Calculation of the distance (in kilometers) between two latitude and longitude coordinates"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))


def fetch_accident_data():
    """Load incident data from database (Django ORM approach)"""
    with connection.cursor() as cursor:
        # Search for basic information about the accident
        cursor.execute("""
            SELECT a.ACCIDENT_NO, a.SEVERITY, n.LATITUDE, n.LONGITUDE
            FROM accident_data a
            JOIN accident_node n ON a.ACCIDENT_NO = n.ACCIDENT_NO
            WHERE n.LATITUDE IS NOT NULL AND n.LONGITUDE IS NOT NULL
        """)
        accidents = cursor.fetchall()

        # Querying death statistics
        cursor.execute("""
            SELECT ACCIDENT_NO, COUNT(*) as deaths
            FROM accident_person_data
            WHERE INJ_LEVEL = 1
            GROUP BY ACCIDENT_NO
        """)
        deaths = {row[0]: row[1] for row in cursor.fetchall()}

    # Convert to DataFrame
    df = pd.DataFrame(accidents, columns=["ACCIDENT_NO", "SEVERITY", "LATITUDE", "LONGITUDE"])
    df["NO_PERSONS_KILLED"] = df["ACCIDENT_NO"].map(deaths).fillna(0).astype(int)
    return df

@api_view(['GET'])
def analyze_accidents(request):
    """Analyzing accident data in the vicinity of the coordinates"""
    try:
        # Parse request parameters (format: ?coords=lat1,lon1|lat2,lon2&radius=1.0)
        coords = [
            tuple(map(float, point.split(',')))
            for point in request.GET.get('coords', '').split('|')
            if point
        ]
        radius = float(request.GET.get('radius', 1.0))

        if not coords:
            return JsonResponse({"error": "No coordinates provided"}, status=400)

        # Acquire and analyze data
        accident_df = fetch_accident_data()
        results = []

        for lat, lon in coords:
            # Calculate distance and filter
            accident_df['distance'] = accident_df.apply(
                lambda row: haversine(lat, lon, row['LATITUDE'], row['LONGITUDE']),
                axis=1
            )
            nearby = accident_df[accident_df['distance'] <= radius]

            # Statistical indicators
            stats = {
                "coordinate": {"latitude": lat, "longitude": lon},
                "total_accidents": len(nearby),
                "serious_accidents": len(nearby[nearby["SEVERITY"] == 1]),
                "total_deaths": int(nearby["NO_PERSONS_KILLED"].sum()),
                "death_rate": round(nearby["NO_PERSONS_KILLED"].sum() / len(nearby), 4) if len(nearby) > 0 else 0
            }
            results.append(stats)

        return JsonResponse({"results": results})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_postcode_scores(request):
    data = VicPostcodeScore.objects.all().values()
    return JsonResponse(list(data), safe=False)

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
