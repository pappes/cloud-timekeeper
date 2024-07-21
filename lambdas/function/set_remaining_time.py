from google.cloud import storage
import json

def set_remaining_time(data, bucket_name, filename, storage_client=None):
  """Writes JSON data to a file in a Cloud Storage bucket.

  Args:
    data: The JSON data to write (as a dictionary).
    bucket_name: The name of the Cloud Storage bucket.
    filename: The filename to use for the uploaded file.
    storage_client: An optional Google Cloud Storage client object for mocking.
  """

  if not storage_client:
    storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(filename)
  blob.upload_from_string(json.dumps(data), content_type='application/json')

