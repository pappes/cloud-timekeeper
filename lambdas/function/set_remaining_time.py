from google.cloud import storage
import functions_framework
from flask import abort
import json


TOURNAMENT = 'tournament'
ROUND = 'round'
FINISH = 'finish_time'
REMAINING = 'time_remaining'

def set_remaining_time(request, storage_client=None):
  """HTTP Cloud Function that writes JSON data to a file in a Cloud Storage bucket.

  Args:
    request (flask.Request): The request object.
    <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    expected contents:
      tournament: The filename to use for the uploaded file.
      round: The blinds round currently in progress.
      finish_time: When unpaused the time when the current round will finish.
      time_remaining: When paused the number of seconds on the clock.
      storage_client: An optional Google Cloud Storage client object for mocking.

  Returns:
    The JSON data, or a map of errors.
  """
  request_json = request.get_json(silent=True)
  request_args = request.args

  tournament=None
  round=None
  finish_time=None
  time_remaining=None

  if request_json:
    if TOURNAMENT in request_json:
      tournament = request_json[TOURNAMENT]
    if ROUND in request_json:
      round = request_json[ROUND]
    if FINISH in request_json:
      finish_time = request_json[FINISH]
    if REMAINING in request_json:
      time_remaining = request_json[REMAINING]

  if request_args:
    if TOURNAMENT in request_args:
      tournament = request_args[TOURNAMENT]
    if ROUND in request_args:
      round = request_args[ROUND]
    if FINISH in request_args:
      finish_time = request_args[FINISH]
    if REMAINING in request_args:
      time_remaining = request_args[REMAINING]

  if (tournament is None) or (round is None) :
      return abort(400, json.dumps({"error": "You need to tell me what you are doing!"}))

  if not storage_client:
    storage_client = storage.Client()
  try:
    data = {"round": round, "finish_time": finish_time, "time_remaining": time_remaining}    
    json_string = json.dumps(data)

    bucket = storage_client.bucket("bpt-timer")
    blob = bucket.blob(tournament)

    blob.upload_from_string(data=json_string, content_type="application/json")
    return json_string;
  except Exception as e:
    print(f"Error writing data to storage bucket: {e}")
    return abort(500, json.dumps({"error": str(e)}))

