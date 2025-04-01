from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_example(request):
    data = {"message": "Hello from Django!"}
    return Response(data)