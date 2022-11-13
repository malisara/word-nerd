from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Language
from .serializers import LanguageSerializer
from decks.models import Deck


class AllLanguagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        languages = Language.objects.all().order_by('name')
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)


class AddLanguageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            chosen_language = Language.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Language instance does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.languages.filter(id=pk).count() == 0:
            chosen_language.users.add(request.user)
            Deck.objects.create(owner=request.user, language=chosen_language)
            return Response({'detail': 'New language added.'},
                            status=status.HTTP_201_CREATED)

        return Response({'detail': 'Language is already selected.'},
                        status=status.HTTP_409_CONFLICT)
