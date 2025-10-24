from django.db.models.query import QuerySet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import (
    FilterSet,
    CharFilter
)
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RoleBasicSerializer,RoleSerializer
from .models import Role
from telemed.utils.custom_paginaation import CustomPagination

class RoleFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    description_long_text = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Role
        fields = {
            'id': ['exact', 'in'],
            'date_created':['exact', 'range'],
            'date_modified':['exact', 'range'],
            'title': ['exact', 'icontains', 'istartswith', 'iendswith'],
            'archive': ['exact', 'icontains', 'istartswith', 'iendswith', 'in', 'isnull'],
        }

class RoleCreate(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter , filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = ['title']
    permission_classes = [AllowAny]

    def perform_create(self,serializer):
        instance = serializer.save()

    def list(self,request,*args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset,many = True)
        return Response(serializer.data)
    
class RoleList(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleBasicSerializer
    filter_backends = [filters.SearchFilter , filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = ['title']
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def list(self,request,*args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset,request, view = self)
        serializer = self.get_serializer(page,many = True)
        return paginator.get_paginated_response(serializer.data)
    
class RoleRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    
    def perform_update(self, serializer):
        instance = serializer.save()
        return instance
    
    def perform_destroy(self, instance):
        instance.archive = True
        instance.save()
        return instance