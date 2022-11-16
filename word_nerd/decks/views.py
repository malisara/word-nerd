from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from decks.models import Deck
from flashcards.models import Language
from .serializers import NewDeckSerializer


class NewDeckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NewDeckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({'detail': 'New deck created.'},
                            status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid data',
                        'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
