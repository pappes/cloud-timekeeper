
import unittest
from unittest.mock import Mock, patch
import json

from get_remaining_time import get_remaining_time


class TestReadJsonFromBucket(unittest.TestCase):

  @patch('get_remaining_time.storage.Client')  # Patch the storage.Client class
  def test_success(self, mocked_client):
    """Tests successful download and parsing of JSON data."""
    mocked_blob = Mock()
    mocked_blob.download_as_string.return_value = '{"key": "value"}'
    mocked_client.return_value = Mock(return_value=Mock(blob=Mock(return_value=mocked_blob)))

    data = get_remaining_time('bucket-name', 'data.json', mocked_client)

    self.assertEqual(data, {'key': 'value'})
    mocked_client.assert_called_once_with()  # Assert Cloud Storage client is created

  @patch('get_remaining_time.storage.Client')
  def test_download_error(self, mocked_client):
    """Tests error handling during download."""
    mocked_client.return_value = Mock(return_value=Mock(blob=Mock(download_as_string=Mock(side_effect=Exception('download error')))))

    data = get_remaining_time('bucket-name', 'data.json', mocked_client)

    self.assertIsNone(data)

  @patch('get_remaining_time.json.loads')
  def test_parse_error(self, mock_parse):
    """Tests error handling during JSON parsing."""
    mock_blob = Mock()
    mock_blob.download_as_string.return_value = 'invalid_json'
    mocked_client = Mock(return_value=Mock(blob=Mock(return_value=mock_blob)))

    mock_parse.side_effect = json.JSONDecodeError('Invalid JSON')

    data = get_remaining_time('bucket-name', 'data.json', mocked_client)

    self.assertIsNone(data)
    mock_parse.assert_called_once_with('invalid_json')


if __name__ == '__main__':
  unittest.main()