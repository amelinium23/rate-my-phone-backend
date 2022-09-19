from typing import Dict, List
from google.cloud import storage
from werkzeug.datastructures import FileStorage


def upload_to_images_storage(files: Dict[str, FileStorage],
                             folder_name: str, client: storage.Client) -> List[str]:
  file_names: List[str] = []
  bucket: storage.Bucket = list(client.list_buckets())[0]
  for _, file_data in files.items():
    blob = bucket.blob(f"{folder_name}/{file_data.filename}")
    blob.upload_from_file(file_data.stream, content_type="image/jpeg")
    file_names.append(blob.public_url)
  return file_names
