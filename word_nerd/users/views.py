from rest_framework.generics import CreateAPIView

from .serializers import RegisterSerializer


class RegisterUserApi(CreateAPIView):
    serializer_class = RegisterSerializer
