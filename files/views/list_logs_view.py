from rest_framework.generics import ListAPIView
from files.models.log_operation import LogOperation
from files.serializers.log_operation_serializer import LogOperationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class LogOperationListAPIView(ListAPIView):
    queryset = LogOperation.objects.all().order_by('-timestamp')
    serializer_class = LogOperationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['operation_type', 'status', 'file']
    ordering_fields = ['timestamp']
