from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from files.models import File
from files.models.log_operation import LogOperation
from files.services.gcs_signed_url_generator import generate_signed_url
from django.utils.timezone import now


class FileDownloadAPIView(APIView):
    def get(self, request, file_id):
        file_instance = get_object_or_404(File, id=file_id)

        signed_url = generate_signed_url(file_instance.bucket_path)

        if not signed_url:
            # Hatalı log
            LogOperation.objects.create(
                file=file_instance,
                operation_type="DOWNLOAD",
                status="FAILURE",
                timestamp=now(),
                ip_address=self._get_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details="Signed URL oluşturulamadı."
            )
            return Response({"error": "Dosya bağlantısı oluşturulamadı."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Başarılı log
        LogOperation.objects.create(
            file=file_instance,
            operation_type="DOWNLOAD",
            status="SUCCESS",
            timestamp=now(),
            ip_address=self._get_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            details="Dosya için signed URL oluşturuldu."
        )

        return Response({"signed_url": signed_url}, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
