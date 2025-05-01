

from rest_framework.decorators import api_view
from .models import AccidentData, AccidentNode, AccidentPersonData
from geopy.distance import geodesic
from .models import VicPostcodeScore
from django.http import JsonResponse
from django.db import connection
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from shapely.wkt import loads as load_wkt
from shapely.geometry import Point
from .models import UVData
import datetime
from django.db.models.functions import TruncDate
from django.db.models import Max
from .models import VicCrimeScore
from .models import Facility
from django.db.models import Count
@api_view(['GET'])
def get_postcode_by_coordinate(request):
    try:
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

    user_point = Point(lng, lat)

    for area in VicPostcodeScore.objects.all():
        try:
            polygon = load_wkt(area.geometry)
            if polygon.contains(user_point):
                return JsonResponse({
                    'postcode': area.postcode,
                    'traffic_score': area.traffic_score,
                    'crime_score': area.crime_score,
                    'facility_count': area.facility_count
                })
        except Exception as e:
            continue

    return JsonResponse({'error': 'No matching area found'}, status=404)



def haversine(lat1, lon1, lat2, lon2):
    """Calculation of the distance (in kilometers) between two latitude and longitude coordinates"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))


def fetch_accident_data():
    """Load accident data using Django ORM"""

    # Get all nodes with valid coordinates
    nodes = AccidentNode.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )

    accident_info = []

    # For each node, retrieve corresponding accident details
    for node in nodes:
        try:
            accident = AccidentData.objects.get(accident_no=node.accident_no)
            accident_info.append([
                accident.accident_no,
                accident.severity,
                node.latitude,
                node.longitude
            ])
        except AccidentData.DoesNotExist:
            # If accident record does not exist for the node, skip it
            continue

    # Count number of fatalities (INJ_LEVEL = 1) grouped by accident number
    death_counts = (
        AccidentPersonData.objects
        .filter(inj_level=1)
        .values('accident_no')
        .annotate(deaths_count=Count('accident_no'))
    )

    # Convert to dictionary for fast lookup
    death_dict = {item['accident_no']: item['deaths_count'] for item in death_counts}

    # Create a pandas DataFrame with the collected data
    df = pd.DataFrame(accident_info, columns=["ACCIDENT_NO", "SEVERITY", "LATITUDE", "LONGITUDE"])

    # Add NO_PERSONS_KILLED column using the death dictionary
    df["NO_PERSONS_KILLED"] = df["ACCIDENT_NO"].map(death_dict).fillna(0).astype(int)

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
def get_crime_scores(request):
    data = VicCrimeScore.objects.all().values()
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

@api_view(['GET'])
def get_uv_index_by_year(request):
    try:
        year = int(request.GET.get('year'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid or missing year'}, status=400)

    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year + 1, 1, 1)

    uv_data = (
        UVData.objects
        .filter(date_time__gte=start_date, date_time__lt=end_date)
        .annotate(day=TruncDate('date_time'))
        .values('day')
        .annotate(max_uv=Max('uv_index'))
        .order_by('day')
    )

    results = [
        {'date': entry['day'].strftime('%Y-%m-%d'), 'max_uv_index': entry['max_uv']}
        for entry in uv_data
    ]

    return JsonResponse({'year': year, 'daily_max_uv': results})

@api_view(['GET'])
def facilities_by_postcode(request):
    postcode = request.GET.get('postcode')
    if not postcode:
        return JsonResponse({"error": "postcode is required"}, status=400)

    try:
        area = VicPostcodeScore.objects.get(postcode=postcode)
        polygon = load_wkt(area.geometry)
    except VicPostcodeScore.DoesNotExist:
        return JsonResponse({"error": "Postcode not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Invalid geometry: {e}"}, status=500)

    facilities = Facility.objects.filter(
        longitude__isnull=False, latitude__isnull=False
    )

    result = []
    for f in facilities:
        try:
            point = Point(f.longitude, f.latitude)
            if polygon.contains(point):
                result.append({
                    "name": str(f.name),
                    "type": str(f.ftype),
                    "subtype": str(f.featsubtyp),
                    "longitude": float(f.longitude),
                    "latitude": float(f.latitude)
                })
        except:
            continue
    return JsonResponse(result, safe=False)