from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserPreferencesSerializer

class UserPreferencesView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserPreferencesSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserPreferencesSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)