from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from files.models import File
from files.serializers import FileSerializer

class FileListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        files = File.objects.all().order_by('-uploaded_at')
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
