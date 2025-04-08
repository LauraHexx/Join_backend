from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from boards_app.models import Board
from boards_app.api.serializers import BoardSerializer


# Create your views here.


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(created_by=user)
