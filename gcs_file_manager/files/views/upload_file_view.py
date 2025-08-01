from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from files.serializers import FileSerializer
from files.models import File
from files.models.log_operation import LogOperation
from files.services.gcs_uploader import upload_file_to_gcs
from files.tasks.generate_pdf_preview import generate_pdf_preview
from django.utils.timezone import now

class FileUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']

            try:
                # 1. GCS'ye yükle
                gcs_path = upload_file_to_gcs(file_obj)

                # 2. Veritabanına kaydet
                file_instance = File.objects.create(
                    original_filename=file_obj.name,
                    bucket_path=gcs_path,
                    size=file_obj.size,
                    mime_type=file_obj.content_type
                )

                # 3. Log kaydı
                LogOperation.objects.create(
                    file=file_instance,
                    operation_type='UPLOAD',
                    status='SUCCESS',
                    timestamp=now(),
                    ip_address=self._get_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    details='Dosya başarıyla yüklendi.'
                )

                # 4. PDF ise önizleme task'ı
                if file_obj.content_type == 'application/pdf':
                    generate_pdf_preview.delay(file_instance.id)

                response_data = FileSerializer(file_instance).data
                return Response(response_data, status=status.HTTP_201_CREATED)

            except Exception as e:

                LogOperation.objects.create(
                    file=None,
                    operation_type='UPLOAD',
                    status='FAILURE',
                    timestamp=now(),
                    ip_address=self._get_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    details=f"Yükleme hatası: {str(e)}"
                )
                return Response({"error": "Dosya yüklenirken bir hata oluştu."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
