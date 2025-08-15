import uuid
from google.cloud import storage
from django.conf import settings

def upload_file_to_gcs(file_obj):

    client = storage.Client()
    bucket = client.bucket(settings.GCS_BUCKET_NAME)

    unique_filename = f"{uuid.uuid4()}_{file_obj.name}"
    blob = bucket.blob(unique_filename)
    blob.upload_from_file(file_obj, content_type=file_obj.content_type)

    return unique_filename
