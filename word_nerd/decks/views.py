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
                            status=status.HTTP_404_NOT_FOUND)

        decks = Deck.objects.filter(language=language, owner=request.user)
        serializer = DeckSerializer(decks, many=True)
        return Response({'decks': serializer.data}, status=status.HTTP_200_OK)


class EditDeckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            deck = Deck.objects.get(id=pk, owner=request.user)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DeckSerializer(deck, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Deck is updated.'})
        return Response(
            {'detail': 'Invalid data', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


class DeleteDeckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            deck = Deck.objects.get(id=pk, owner=request.user)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        message = f"Deck '{deck.name}' is deleted."
        deck.delete()
        return Response({'detail': message})
