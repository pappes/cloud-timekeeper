
from google.cloud import storage
import json


def get_remaining_time(bucket_name, filename, storage_client=None):
  """Reads a JSON file from a Cloud Storage bucket and returns the data.

  Args:
    bucket_name: The name of the Cloud Storage bucket.
    filename: The filename of the JSON file to read.
    storage_client: An optional Google Cloud Storage client object for mocking.

  Returns:
    A dictionary containing the parsed JSON data, or None if an error occurs.
  """

  if not storage_client:
    storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(filename)

  try:
    data = blob.download_as_string()
    return json.loads(data)
  except Exception as e:
    print(f"Error reading file: {e}")
    return None
