from django.db import models
from files.models.file import File


class LogOperation(models.Model):
    class OperationType(models.TextChoices):
        UPLOAD = "UPLOAD", "Upload"
        DELETE = "DELETE", "Delete"
        PDF_PREVIEW = "PDF_PREVIEW", "PDF Preview"
        DOWNLOAD = "DOWNLOAD", "Download"

    class Status(models.TextChoices):
        STARTED = "started", "Started"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)
    operation_type = models.CharField(max_length=50, choices=OperationType.choices)
    status = models.CharField(max_length=50, choices=Status.choices)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation_type} → {self.status} ({self.timestamp})"
