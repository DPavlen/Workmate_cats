from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Breed, Cat
from .serializers import BreedSerializer, CatSerializer


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet пород котов."""
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class CatViewSet(viewsets.ModelViewSet):
    """Кастомный основной ViewSet котов."""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (IsAuthenticated),
