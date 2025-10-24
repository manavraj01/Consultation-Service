from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer, MessageBasicSerializer
from telemed.utils.custom_paginaation import CustomPagination
from rest_framework.permissions import AllowAny

class MessageFilter(FilterSet):
    author_username = CharFilter(field_name='author__username', lookup_expr='icontains')
    author_role_title = CharFilter(field_name='author_role__title', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = {
            'id': ['exact', 'in'],
            'consultation': ['exact', 'in'],
            'date_created': ['exact', 'range'],
            'archive': ['exact', 'isnull'],
        }



class MessageCreate(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = ['author__username', 'author_role__title']
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MessageList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageBasicSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = '__all__'
    search_fields = ['author__username', 'author_role__title']
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        consultation_id = request.query_params.get('consultation')
        role_id = request.query_params.get('role')

        # Validate IDs before filtering
        try:
            if consultation_id:
                consultation_id = int(consultation_id)
                queryset = queryset.filter(consultation_id=consultation_id)
            if role_id:
                role_id = int(role_id)
                queryset = queryset.filter(author_role_id=role_id)
        except ValueError:
            return Response({"error": "Consultation ID and Role ID must be integers."}, status=400)

        queryset = queryset.order_by('date_created')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)




class MessageRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MessageSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        return instance

    def perform_destroy(self, instance):
        instance.archive = True
        instance.save()
        return instance
