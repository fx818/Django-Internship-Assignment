from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .tasks import send_welcome_email
from .serializers import RegisterSerializer
import logging

# Create your views here.

logger = logging.getLogger(__name__)

class PublicAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "This is a public endpoint."})

class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}. This is a protected endpoint."})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = serializer.validated_data.get('email', None)
            username = serializer.validated_data['username']
            if email:
                try:
                    send_welcome_email.delay(email, username)
                except Exception as e:
                    logger.error(f"Failed to send welcome email: {e}")
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
