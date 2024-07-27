import flask
import unittest
from unittest.mock import Mock

from main import set_remaining_time

class TestSetRemainingTime(unittest.TestCase):
  # sample data
  tournament = "Aug-2024"
  round = "Round 3"
  finish_time = "2024-08-15T12:00:00"
  time_remaining = "treefidy(350s)"
  metadata = '{"message" : "Last round for rebuys"}'
  json_payload = {
      "tournament": tournament,
      "round": round,
      "finish_time": finish_time,
      "time_remaining": time_remaining,
      "metadata": metadata,
    }

  @unittest.mock.patch("main.storage.Client")
  def test_write_json_to_bucket_with_mocked_client(self, mock_client):
    """Tests writing with a mocked client."""
    # Arrange.
    mocked_blob = Mock()
    mocked_blob.upload_from_string.return_value = "mocked_blob"
    mocked_bucket = Mock()
    mocked_bucket.blob.return_value = mocked_blob
    mocked_client = Mock()
    mocked_client.bucket.return_value = mocked_bucket
    mock_client.return_value = mocked_client

    request = Mock()
    request.get_json.return_value = self.json_payload
    request.args = None

    expected_output = '{"tournament": "Aug2024", "round": "Round3", "finish_time": "2024-08-15T12:00:00", "time_remaining": "350", "metadata": "{\\"message\\" : \\"Last round for rebuys\\"}"}'

    # Act.
    data = set_remaining_time(request)

    # Assert.
    mocked_client.bucket.assert_called_once_with("bpt-timer")
    mocked_bucket.blob.assert_called_once_with("Aug2024")
    mocked_blob.upload_from_string.assert_called_once_with(data=expected_output, content_type="application/json")
    self.assertEqual(data, expected_output)

  @unittest.mock.patch("main.abort")
  @unittest.mock.patch("main.storage.Client")
  def test_validation_error(self, mock_client, mock_abort):
    """Tests error handling during input validation."""
    # Arrange.
    request = Mock()
    request.get_json.return_value = self.json_payload.copy()
    request.get_json.return_value["finish_time"] = "midnight(12:00)"
    request.args = None

    expected_output = '{"error": "Invalid isoformat string: \'midnight(12:00)\'"}'

    # Act.
    data = set_remaining_time(request)

    # Assert.
    mock_abort.assert_called_once_with(400, expected_output)
    self.assertIs(data, mock_abort())

  @unittest.mock.patch("main.abort")
  @unittest.mock.patch("main.storage.Client")
  def test_upload_error(self, mock_client, mock_abort):
    """Tests error handling during upload."""
    # Arrange.
    mocked_blob = Mock()
    mocked_blob.upload_from_string.side_effect=Exception("testing upload error")
    mocked_bucket = Mock()
    mocked_bucket.blob.return_value = mocked_blob
    mocked_client = Mock()
    mocked_client.bucket.return_value = mocked_bucket
    mock_client.return_value = mocked_client
    request = Mock()
    request.get_json.return_value = self.json_payload
    request.args = None

    expected_output = '{"error": "testing upload error"}'

    # Act.
    data = set_remaining_time(request)

    # Assert.
    mock_abort.assert_called_once_with(500, expected_output)
    self.assertIs(data, mock_abort())

  @unittest.mock.patch("main.abort")
  def test_parameter_error(self, mock_abort):
    """Tests error in invocation parameters."""
    # Arrange.
    request = Mock()
    request.get_json.return_value = None
    request.args = None

    expected_output = '{"error": "You need to tell me what you are doing!"}'

    # Act.
    data = set_remaining_time(request)

    # Assert.
    mock_abort.assert_called_once_with(400, expected_output)
    self.assertIs(data, mock_abort())

if __name__ == "__main__":
  unittest.main()

