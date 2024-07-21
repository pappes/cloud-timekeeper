
from google.cloud import storage
import functions_framework
from flask import abort
import json

TOURNAMENT = 'tournament'

@functions_framework.http
def get_remaining_time(request, storage_client=None):
  """HTTP Cloud Function that reads a JSON file from a Cloud Storage bucket and returns the data.

  Args:
    request (flask.Request): The request object.
    <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    expected contents:
      tournament: The filename of the JSON file to read.
      storage_client: An optional Google Cloud Storage client object for mocking.

  Returns:
    The JSON data, or a map of errors.
  """


  request_json = request.get_json(silent=True)
  request_args = request.args

  if request_json and TOURNAMENT in request_json:
      tournament = request_json[TOURNAMENT]
  elif request_args and TOURNAMENT in request_args:
      tournament = request_args[TOURNAMENT]
  else:
      return abort(400, json.dumps({"error": "You need to tell me what you are looking for!"}))


  if not storage_client:
    storage_client = storage.Client()
  try:
    bucket = storage_client.bucket("bpt-timer")
    blob = bucket.blob(tournament)

    return blob.download_as_string()
  except Exception as e:
    print(f"Error accessing data from storage bucket: {e}")
    return abort(500, json.dumps({"error": str(e)}))


