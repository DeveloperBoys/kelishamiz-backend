from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from .filters import ClassifiedFilter
from apps.user_searches.models import SearchQuery
from .models import (
    APPROVED,
    Category,
    Classified
)
from apps.permissions.permissions import (
    ClassifiedOwner,
    IsAdminOrReadOnly,
    EditClassifiedPermission
)
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedOwnerSerializer,
    ClassifiedSerializer,
    DeleteClassifiedSerializer,
    ClassifiedCreateSerializer
)
from apps.classified_statistics.serializers import ClassifiedLikeSerializer
from apps.classified_statistics.models import ClassifiedLike, ClassifiedView


class ClassifiedPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


@method_decorator(cache_page(60*15), name='dispatch')
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


@method_decorator(cache_page(60*15), name='dispatch')
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


@method_decorator(cache_page(60*15), name='dispatch')
class ClassifiedListView(generics.ListAPIView):
    queryset = Classified.objects.filter(
        status=APPROVED).order_by('-created_at')
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = ClassifiedFilter
    pagination_class = ClassifiedPagination

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        search_query = self.request.query_params.get('search')
        if search_query and self.request.user.is_authenticated:
            SearchQuery.objects.create(
                user=self.request.user,
                query=search_query
            )

        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


@method_decorator(cache_page(60*15), name='dispatch')
class ClassifiedDetailView(generics.RetrieveAPIView):
    queryset = Classified.objects.filter(status=APPROVED)
    serializer_class = ClassifiedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_object(self):
        obj = super().get_object()
        ClassifiedView.objects.create(classified=obj)

        return obj


@method_decorator(cache_page(60*15), name='dispatch')
class DeleteClassifiedView(generics.DestroyAPIView):
    queryset = Classified.objects.all()
    serializer_class = DeleteClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, permissions.IsAdminUser]


@method_decorator(cache_page(60*15), name='dispatch')
class CreateClassifiedView(generics.CreateAPIView):
    serializer_class = ClassifiedCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)


@method_decorator(cache_page(60*15), name='dispatch')
class ClassifiedLikeView(generics.GenericAPIView):
    serializer_class = ClassifiedLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return ClassifiedLike.objects.filter(
                classified_id=self.kwargs['pk']
            )
        except:
            return None

    def post(self, request, *args, **kwargs):
        obj, created = ClassifiedLike.objects.get_or_create(
            classified_id=self.kwargs['pk'],
            user=self.request.user
        )
        obj.is_active = True
        obj.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        obj, created = ClassifiedLike.objects.get_or_create(
            classified_id=self.kwargs['pk'],
            user=self.request.user
        )
        obj.is_active = False
        obj.save()
        return Response(status=status.HTTP_202_ACCEPTED)


@method_decorator(cache_page(60*15), name='dispatch')
class EditClassifiedView(generics.RetrieveUpdateAPIView):
    serializer_class = ClassifiedCreateSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, EditClassifiedPermission]

    def get_queryset(self):
        try:
            return Classified.objects.filter(classified=self.kwargs['pk'])
        except:
            return None


@method_decorator(cache_page(60*15), name='dispatch')
class ClassifiedOwnerView(generics.ListAPIView):
    serializer_class = ClassifiedListSerializer

    def get_queryset(self):
        return Classified.objects.get(pk=self.kwargs['pk'], status=APPROVED)

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        user = instance.owner
        classifieds = Classified.objects.filter(
            owner=user, status=APPROVED).order_by('-created_at')

        data = {
            "owner": ClassifiedOwnerSerializer(user).data,
            "classifieds": self.get_serializer(classifieds, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)
