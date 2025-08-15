from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from files.models import File
from files.models.log_operation import LogOperation
from google.cloud import storage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.timezone import now


class FileDeleteAPIView(APIView):
    def delete(self, request, file_id):
        file_instance = get_object_or_404(File, id=file_id)

        try:
            # GCS'den sil
            client = storage.Client()
            bucket = client.bucket(settings.GCS_BUCKET_NAME)
            blob = bucket.blob(file_instance.bucket_path)
            blob.delete()

            # Log işlemi
            LogOperation.objects.create(
                file=file_instance,
                operation_type="DELETE",
                status="SUCCESS",
                timestamp=now(),
                ip_address=self._get_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                details="Dosya başarıyla silindi."
            )

            # Veritabanından sil
            file_instance.delete()

            return Response({"message": "Dosya başarıyla silindi."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            # Hata loglama
            LogOperation.objects.create(
                file=file_instance,
                operation_type="DELETE",
                status="FAILURE",
                timestamp=now(),
                ip_address=self._get_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                details=f"Silme işlemi başarısız: {str(e)}"
            )
            return Response({"error": "Dosya silinirken bir hata oluştu."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
