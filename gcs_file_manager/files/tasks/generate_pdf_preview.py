from celery import shared_task
from files.models.file import File
from files.models.log_operation import LogOperation
import fitz
import os

@shared_task
def generate_pdf_preview(file_id):
    try:
        file = File.objects.get(id=file_id)

        log = LogOperation.objects.create(
            file=file,
            operation_type=LogOperation.OperationType.PDF_PREVIEW,
            status=LogOperation.Status.STARTED,
            details="PDF önizleme analizi başlatıldı."
        )

        # PDF dosyasını indir
        import requests
        response = requests.get(file.gcs_url)

        if response.status_code != 200:
            raise Exception(f"PDF indirilemedi. HTTP Status: {response.status_code}")

        with open("temp.pdf", "wb") as f:
            f.write(response.content)

        # PDF dosyasını analiz et
        doc = fitz.open("temp.pdf")
        page_count = doc.page_count
        doc.close()

        # Geçici dosyayı temizle
        os.remove("temp.pdf")

        log.status = LogOperation.Status.COMPLETED
        log.details = f"PDF sayfa sayısı: {page_count}"
        log.save()

    except File.DoesNotExist:
        LogOperation.objects.create(
            file=None,
            operation_type=LogOperation.OperationType.PDF_PREVIEW,
            status=LogOperation.Status.FAILED,
            details=f"ID {file_id} ile eşleşen dosya bulunamadı."
        )
    except Exception as e:
        LogOperation.objects.create(
            file_id=file_id,
            operation_type=LogOperation.OperationType.PDF_PREVIEW,
            status=LogOperation.Status.FAILED,
            details=str(e)
        )
