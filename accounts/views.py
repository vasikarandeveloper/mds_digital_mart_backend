from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):

    pass


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            'username': request.user.username,
            'email': request.user.email
        })


class AdminCheckView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.is_staff:

            return Response({
                'is_admin': True
            })

        return Response({
            'is_admin': False
        })
