from google.cloud import storage
from django.conf import settings
from datetime import timedelta
from google.cloud.storage.blob import Blob
from google.cloud.storage.bucket import Bucket
from typing import Optional
import datetime


def generate_signed_url(bucket_path: str, expiration_minutes: int = 5) -> Optional[str]:
    try:
        client = storage.Client()
        bucket: Bucket = client.bucket(settings.GCS_BUCKET_NAME)
        blob: Blob = bucket.blob(bucket_path)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=expiration_minutes),
            method="GET"
        )
        return url
    except Exception as e:

        print(f"Signed URL oluşturulamadı: {e}")
        return None
