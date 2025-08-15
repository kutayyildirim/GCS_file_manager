from rest_framework import serializers
from files.models.log_operation import LogOperation

class LogOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogOperation
        fields = [
            'id',
            'file',
            'operation_type',
            'status',
            'timestamp',
            'details'
        ]
        read_only_fields = fields

