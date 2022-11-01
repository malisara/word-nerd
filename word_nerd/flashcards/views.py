from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Language
from .serializers import LanguageSerializer


class AllLanguagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        languages = Language.objects.all().order_by('name')
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)
