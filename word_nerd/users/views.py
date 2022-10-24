from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .serializers import RegisterUserSerializer


class RegisterUserAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class LogoutUserAPIView(CreateAPIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({'detail': "logout successful"})
        return Response({'detail': "you weren't logged in"}, status=status.HTTP_409_CONFLICT)
