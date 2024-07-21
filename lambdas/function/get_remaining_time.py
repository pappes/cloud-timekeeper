
from google.cloud import storage
import json


def get_remaining_time(tournament, storage_client=None):
  """Reads a JSON file from a Cloud Storage bucket and returns the data.

  Args:
    tournament: The filename of the JSON file to read.
    storage_client: An optional Google Cloud Storage client object for mocking.

  Returns:
    A the JSON data, or a map of errors.
  """

  if not storage_client:
    storage_client = storage.Client()
  try:
    bucket = storage_client.bucket("bpt")
    blob = bucket.blob(tournament)

    return blob.download_as_string()
  except Exception as e:
    print(f"Error accessing data from storage bucket: {e}")
    return json.dumps({"error": str(e)})
