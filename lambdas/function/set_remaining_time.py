from google.cloud import storage
import json

def set_remaining_time(tournament, round, finish_time=None, time_remaining=None,storage_client=None):
  """Writes JSON data to a file in a Cloud Storage bucket.

  Args:
    tournament: The filename to use for the uploaded file.
    round: The blinds round currently in progress.
    finish_time: When unpaused the time when the current round will finish.
    time_remaining: When paused the number of seconds on the clock.
    storage_client: An optional Google Cloud Storage client object for mocking.

  Returns:
    A the JSON data, or a map of errors.
  """

  if not storage_client:
    storage_client = storage.Client()
  try:
    data = {"round": round, "finish_time": finish_time, "time_remaining": time_remaining}    
    json_string = json.dumps(data)

    bucket = storage_client.bucket("bpt")
    blob = bucket.blob(tournament)

    blob.upload_from_string(data=json_string, content_type="application/json")
    return json_string;
  except Exception as e:
    print(f"Error writing data to storage bucket: {e}")
    return json.dumps({"error": str(e)})

