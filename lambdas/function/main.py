from google.cloud import storage
from flask import abort
from datetime import datetime
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
      tournament:     The filename to use for the uploaded file. (Mandatory)
      round:          The name of the currently active timer for the tournament.
      finish_time:    The time when the current round will finish (only use when the timer is not paused).
      time_remaining: The number of seconds on the clock (only use when the timer is not paused).
      metadata:       The up to 2000 chars of freetext

  Returns:
    The JSON data, or a map of errors.
  """
  try:
    time_data = extract_inputs(request)
    json_string = json.dumps(time_data)
  except Exception as e:
    return abort(400, json.dumps({"error": str(e)}))

  try:
    bucket = storage.Client().bucket("bpt-timer")
    blob = bucket.blob(time_data[TOURNAMENT])

    blob.upload_from_string(data=json_string, content_type="application/json")
    return json_string;
  except Exception as e:
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
    for blob in bucket.list_blobs(max_results=1, match_glob=time_data[TOURNAMENT]):
      return blob.download_as_string()
  except Exception as e:
    print(f"Error accessing data from storage bucket: {e}")
    return abort(500, json.dumps({"error": str(e)}))
  return abort(404, '{"error": "This is not the tournament you are looking for"}')




def extract_inputs(request):
  """Verify that the required inputs are present, inputs are in the correct format and discard unauthorised inputs

  Args:
    request (flask.Request): The request object.
    <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    expected contents:
      tournament:       The filename of the JSON file to store timer data in.
                            Required parameter
                            Accepts only alphanumeric characters
                            Limited to 255 characters
      round:            The name of the currently active timer for the tournament.
                            Optional parameter - defaults to "CurrentRound"
                            Accepts only alphanumeric characters
                            Limited to 255 characters
      finish_time:      The time when the current round will finish.
                            Optional parameter - only use when the timer is not paused
                            Must conform to pythons subset of ISO 8601 format
      time_remaining:   The number of seconds on the clock.
                            Optional parameter - only use when the timer is paused
                            Accepts only numeric characters (no negative values)
                            Limited to 255 characters
      meta:             Misc metadata for the timer  
                            Limited to 2000 characters



      tournament: The filename to use for the uploaded file.
      round: The name of the currently active timer for the tournament.
      finish_time: The time when the current round will finish (only use when the timer is not paused).
      time_remaining: The number of seconds on the clock (only use when the timer is not paused).
      storage_client: An optional Google Cloud Storage client object for mocking.

  Returns:
    The JSON data, or a map of errors.
  """
  request_json = request.get_json(silent=True)
  request_args = request.args

  time_data = {
    TOURNAMENT: None,
    ROUND: "CurrentRound",
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
      time_data[META] = request_json[META][0:2000]


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
  stripped_text =  re.sub(r"[^a-zA-Z0-9]", "", text)
  if stripped_text == "":
    return None
  return stripped_text[0:255]

def sanitise_number(text):
  """remove all non-numeric chars"""
  if text is None:
    return None
  stripped_text =  re.sub(r"[^0-9]", "", text)
  if stripped_text == "":
    return None
  return stripped_text[0:255]

def sanitise_time(text):
  """verify the datetime conforms to ISO 8601"""
  if text is None:
    return None
  # Allow exceptions to propogate out.
  stripped_text =  re.sub(r"[Z,T]", " ", text).strip()
  datetime_object = datetime.fromisoformat(stripped_text)

  return datetime_object.isoformat()
