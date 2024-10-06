from http import HTTPStatus

from django.db.models import Avg, Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view
from rest_framework.decorators import action
from rest_framework import mixins, viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from core import permissions
from .filters import FilterBreed
from core.permissions import IsOwnerOrReadOnlyOrAdmin
from .models import Breed, Cat, CatPhoto, CatRating
from .schemas import CUSTOM_BREEDS_SCHEMA, CUSTOM_CAT_SCHEMA, CUSTOM_CAT_RATING_SCHEMA
from .serializers import BreedSerializer, CatSerializer, CatPhotoSerializer, CatUpdateSerializer, CatRatingSerializer, \
    CatAverageSerializer

import logging
logger = logging.getLogger(__name__)


@extend_schema_view(**CUSTOM_BREEDS_SCHEMA)
class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet пород котов."""
    queryset = Breed.objects.select_related("group").all()
    serializer_class = BreedSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterBreed
    filterset_fields = ("name",)


@extend_schema_view(**CUSTOM_CAT_SCHEMA)
class CatViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """Кастомный основной ViewSet котов."""

    queryset = Cat.objects.select_related(
        "breed", "owner").prefetch_related("photos")
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.action == "partial_update":
            return CatUpdateSerializer
        if self.action == "photo":
            return CatPhotoSerializer
        return CatSerializer

    def get_permissions(self):
        """
        Возвращает соответствующие разрешения в зависимости от действия.
        """

        action_permissions = {
            "list": (IsOwnerOrReadOnlyOrAdmin(),),
            "retrieve": (IsOwnerOrReadOnlyOrAdmin(),),
            "create": (IsAuthenticated(),),
            "partial_update": (IsOwnerOrReadOnlyOrAdmin(),),
            "destroy": (IsOwnerOrReadOnlyOrAdmin(),),
        }
        return action_permissions.get(self.action, super().get_permissions())

    def create(self, request, *args, **kwargs):
        """
        Создает нового кота.
        """
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Метод изменения информации о коте.
        """
        user = self.request.user
        if user.is_authenticated:
            cat_id = kwargs.get("pk")

            try:
                cat = Cat.objects.get(id=cat_id, owner=user)
            except Cat.DoesNotExist:
                return Response({
                    "detail": "Кот не найден или не принадлежит текущему пользователю."},
                                status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(cat, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(id=user.id)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Метод удаления информации о коте.
        """
        cat = self.get_object()
        cat_name = cat.name
        cat.delete()
        return Response(
            {"message": f"Кот по имени '{cat_name}' успешно удален"},
            status=status.HTTP_200_OK
        )

    @action(
        methods=("POST",),
        detail=True,
        url_path="photo",
        parser_classes=(MultiPartParser, JSONParser)
    )
    def photo(self, request, pk):
        """
        Метод принимает фото кота формата form-data.
        Добавляется фото к сущности кота/кошка.
        """

        cat = get_object_or_404(Cat, pk=pk)
        serializer = self.get_serializer(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(cat=cat)
        return Response(serializer.data, status=HTTPStatus.CREATED)

@extend_schema_view(**CUSTOM_CAT_RATING_SCHEMA)
class CatRatingView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для управления оценками котов."""

    queryset = CatRating.objects.select_related("cat", "user").all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "get_highest_rated_cats":
            return CatAverageSerializer
        return CatRatingSerializer

    def get_queryset(self):
        """
        Возвращаем все рейтинги, с возможностью фильтрации по коту.
        """
        queryset = self.queryset
        cat_id = self.request.query_params.get("cat", None)
        if cat_id:
            queryset = queryset.filter(cat_id=cat_id)
        return queryset

    def perform_create(self, serializer):
        """
        Добавляем текущего пользователя как автора оценки.
        """
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Получение списка оценок.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Создание новой оценки для кота/кошки.
        """
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Удаление оценки у кота/кошки.
        """
        return self.destroy(request, *args, **kwargs)

    @action(
        methods=("GET",),
        detail=False,
        url_path="highest-rated",
        permission_classes=(AllowAny,)
    )
    def get_highest_rated_cats(self, request):
        """Коты, отсортированные по средней оценке(по убыванию)."""

        cats_with_ratings = Cat.objects.annotate(
            average_rating=Avg("ratings__rating"),
            rating_count=Count("ratings")
        ).filter(rating_count__gt=0).order_by("-average_rating")

        serializer = CatAverageSerializer(cats_with_ratings, many=True)
        return Response(serializer.data)