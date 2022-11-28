from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deck
from .serializers import DeckSerializer, NewDeckSerializer
from django.core.exceptions import ObjectDoesNotExist


class NewDeckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NewDeckSerializer(data=request.data,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({'detail': 'New deck created.'},
                            status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid data.',
                        'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class GetUserDecksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, language_pk):
        try:
            language = request.user.languages.get(id=language_pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Language is not selected.'},
                            status=status.HTTP_400_BAD_REQUEST)

        decks = Deck.objects.filter(language=language, owner=request.user)
        serializer = DeckSerializer(decks, many=True)
        return Response({'decks': serializer.data}, status=status.HTTP_200_OK)
