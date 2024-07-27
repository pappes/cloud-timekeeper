
import unittest
import flask
from unittest.mock import Mock

from main import get_remaining_time


class TestGetRemainingTime(unittest.TestCase):

  @unittest.mock.patch("main.storage.Client")
  def test_success(self, mock_client):
    """Tests successful download and return of JSON data."""
    # Arrange.
    mocked_blob = Mock()
    mocked_blob.download_as_string.return_value = '{"key": "value"}'
    mocked_bucket = Mock()
    mocked_bucket.blob.return_value = mocked_blob
    mocked_client = Mock()
    mocked_client.bucket.return_value = mocked_bucket
    mock_client.return_value = mocked_client
    request = Mock()
    request.get_json.return_value = {"tournament": "data.json"}
    request.args = None

    # Act.
    data = get_remaining_time(request)

    # Assert.
    ##self.assertEqual(data, '{"key": "value"}')
    mocked_client.bucket.assert_called_once_with("bpt-timer")
    mocked_bucket.blob.assert_called_once_with("datajson")
    mocked_blob.download_as_string.assert_called_once()

  @unittest.mock.patch("main.abort")
  def test_parameter_error(self, mock_abort):
    """Tests missing parameters."""
    # Arrange.
    request = Mock()
    request.get_json.return_value = None
    request.args = None

    expected_output = '{"error": "You need to tell me what you are doing!"}'

    # Act.
    data = get_remaining_time(request)

    # Assert.
    mock_abort.assert_called_once_with(400,  expected_output)
    self.assertIs(data, mock_abort())

  @unittest.mock.patch("main.abort")
  @unittest.mock.patch("main.storage.Client")
  def test_download_error(self, mock_client, mock_abort):
    """Tests error handling during download."""
    # Arrange.
    mocked_blob = Mock()
    mocked_blob.download_as_string.side_effect=Exception("testing download error")
    mocked_bucket = Mock()
    mocked_bucket.blob.return_value = mocked_blob
    mocked_client = Mock()
    mocked_client.bucket.return_value = mocked_bucket
    mock_client.return_value = mocked_client
    request = Mock()
    request.get_json.return_value = {"tournament": "data.json"}
    request.args = None

    expected_output = '{"error": "testing download error"}'

    # Act.
    data = get_remaining_time(request)

    # Assert.
    mock_abort.assert_called_once_with(500, expected_output)
    self.assertIs(data, mock_abort())


if __name__ == "__main__":
  unittest.main()