from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Consultation
from .serializers import ConsultationSerializer, ConsultationBasicSerializer
from telemed.utils.custom_paginaation import CustomPagination
from rest_framework.permissions import AllowAny

class ConsultationFilter(FilterSet):
    patient_username = CharFilter(field_name='patient__username', lookup_expr='icontains')
    doctor_username = CharFilter(field_name='doctor__username', lookup_expr='icontains')

    class Meta:
        model = Consultation
        fields = {
            'id': ['exact', 'in'],
            'date_created': ['exact', 'range'],
            'date_modified': ['exact', 'range'],
            'archive': ['exact', 'isnull'],
        }



class ConsultationCreate(ListCreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = ['patient__username', 'doctor__username']
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ConsultationList(ListAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationBasicSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = ['patient__username', 'doctor__username']
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)



class ConsultationRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Consultation.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ConsultationSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        return instance

    def perform_destroy(self, instance):
        instance.archive = True
        instance.save()
        return instance
