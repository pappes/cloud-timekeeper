
import unittest
from unittest.mock import Mock
import json

from get_remaining_time import get_remaining_time


class TestGetRemainingTime(unittest.TestCase):

  @unittest.mock.patch('get_remaining_time.storage.Client')
  def test_success(self, mock_client):
    """Tests successful download and parsing of JSON data."""
    mocked_blob = Mock()
    mocked_blob.download_as_string.return_value = '{"key": "value"}'
    mocked_bucket = Mock()
    mocked_bucket.blob.return_value = mocked_blob
    mock_client.bucket.return_value = mocked_bucket

    data = get_remaining_time('bucket-name', 'data.json', mock_client)

    self.assertEqual(data, {'key': 'value'})
    mock_client.bucket.assert_called_once_with('bucket-name')
    mocked_bucket.blob.assert_called_once_with('data.json')
    mocked_blob.download_as_string.assert_called_once()

  @unittest.mock.patch('get_remaining_time.storage.Client')
  def test_download_error(self, mock_client):
    """Tests error handling during download."""
    mocked_blob = Mock()
    mocked_blob.download_as_string.side_effect=Exception('testing download error')
    mocked_bucket = Mock()
    mocked_bucket.blob.return_value = mocked_blob
    mock_client.bucket.return_value = mocked_bucket

    data = get_remaining_time('bucket-name', 'data.json', mock_client)

    self.assertIsNone(data)

  @unittest.mock.patch('get_remaining_time.storage.Client')
  def test_parse_error(self, mock_client):
    """Tests error handling during JSON parsing."""
    mocked_blob = Mock()
    mocked_blob.download_as_string.return_value = 'invalid_json'
    mocked_bucket = Mock()
    mocked_bucket.blob.return_value = mocked_blob
    mock_client.bucket.return_value = mocked_bucket


    data = get_remaining_time('bucket-name', 'data.json', mock_client)

    self.assertIsNone(data)


if __name__ == '__main__':
  unittest.main()