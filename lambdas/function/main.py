from google.cloud import storage
from flask import abort
import functions_framework
import json
import re


TOURNAMENT = "tournament"
ROUND = "round"
FINISH = "finish_time"
REMAINING = "time_remaining"
META = "metadata"


def set_remaining_time(request):
  """HTTP Cloud Function that writes JSON data to a file in a Cloud Storage bucket.

  Args:
    request (flask.Request): The request object.
    <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    expected contents:
      tournament: The filename to use for the uploaded file.
      round: The name of the currently active timer for the tournament.
      finish_time: The time when the current round will finish (only use when the timer is not paused).
      time_remaining: The number of seconds on the clock (only use when the timer is not paused).
      storage_client: An optional Google Cloud Storage Client python object for mocking.

  Returns:
    The JSON data, or a map of errors.
  """
  try:
    time_data = extract_inputs(request)
    json_string = json.dumps(time_data)
  except Exception as e:
    #print(f"Error writing data to storage bucket: {e}")
    return abort(400, json.dumps({"error": str(e)}))

  try:
    bucket = storage.Client().bucket("bpt-timer")
    blob = bucket.blob(time_data[TOURNAMENT])

    blob.upload_from_string(data=json_string, content_type="application/json")
    return json_string;
  except Exception as e:
    #print(f"Error writing data to storage bucket: {e}")
    return abort(500, json.dumps({"error": str(e)}))


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

  try:
    time_data = extract_inputs(request)
  except Exception as e:
    #print(f"Error reading data from storage bucket: {e}")
    return abort(400, json.dumps({"error": str(e)}))

  try:
    bucket = storage.Client().bucket("bpt-timer")
    blob = bucket.blob(time_data[TOURNAMENT])

    return blob.download_as_string()
  except Exception as e:
    print(f"Error accessing data from storage bucket: {e}")
    return abort(500, json.dumps({"error": str(e)}))




def extract_inputs(request):
  request_json = request.get_json(silent=True)
  request_args = request.args

  time_data = {
    TOURNAMENT: None,
    ROUND: 'default',
    FINISH: None,
    REMAINING: None,
    META: None
  }

  # Extract supplied parameters.
  if request_json:
    if TOURNAMENT in request_json:
      time_data[TOURNAMENT] = sanitise_name(request_json[TOURNAMENT])
    if ROUND in request_json:
      time_data[ROUND] = sanitise_name(request_json[ROUND])
    if FINISH in request_json:
      time_data[FINISH] = sanitise_time(request_json[FINISH])
    if REMAINING in request_json:
      time_data[REMAINING] = sanitise_number(request_json[REMAINING])
    if META in request_json:
      time_data[META] = request_json[META]


  if request_args:
    if TOURNAMENT in request_args:
      time_data[TOURNAMENT] = sanitise_name(request_args[TOURNAMENT])
    if ROUND in request_args:
      time_data[ROUND] = sanitise_name(request_args[ROUND])
    if FINISH in request_args:
      time_data[FINISH] = sanitise_time(request_args[FINISH])
    if REMAINING in request_args:
      time_data[REMAINING] = sanitise_number(request_args[REMAINING])
    if META in request_args:
      time_data[META] = request_args[META]
  
  if (time_data[TOURNAMENT] is None):
    raise Exception("You need to tell me what you are doing!")
  return time_data
  


def sanitise_name(text):
  """remove all non-alphanumic chars"""
  if text is None:
    return None
  stripped_text =  re.sub(r'[^a-zA-Z0-9]', '', text)
  if stripped_text == "":
    return None
  return stripped_text

def sanitise_number(text):
  """remove all non-numeric chars"""
  if text is None:
    return None
  stripped_text =  re.sub(r'[^0-9]', '', text)
  if stripped_text == "":
    return None
  return stripped_text

def sanitise_time(text):
  """remove all non-numeric chars"""
  if text is None:
    return None
  stripped_text =  re.sub(r'[^0-9]', '', text)
  if stripped_text == "":
    return None
  return stripped_text
