from rest_framework import serializers
from files.models import File

ALLOWED_MIME_TYPES = [
    'image/jpeg', 'image/png', 'application/pdf', 'text/plain'
]
MAX_FILE_SIZE_MB = 20


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = File
        fields = ['id', 'original_filename', 'bucket_path', 'mime_type', 'size', 'uploaded_at', 'file']
        read_only_fields = ['id', 'bucket_path', 'uploaded_at', 'size', 'mime_type', 'original_filename']

    def validate_file(self, value):

        if value.content_type not in ALLOWED_MIME_TYPES:
            raise serializers.ValidationError(f"MIME tipi desteklenmiyor: {value.content_type}")

        if value.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Dosya {MAX_FILE_SIZE_MB}MB'den büyük olamaz.")
        return value
