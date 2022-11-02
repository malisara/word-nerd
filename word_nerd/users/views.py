from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .serializers import RegisterUserSerializer


class RegisterUserAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class LogoutUserAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': "Logout successful."})
