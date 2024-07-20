from google.cloud import storage
import json
import unittest
from unittest.mock import Mock, patch

from set_remaining_time import set_remaining_time

class TestWriteJsonToBucket(unittest.TestCase):


    @patch('set_remaining_time.storage.Client')
    def test_write_json_to_bucket_with_mocked_client(self, mock_client):
        """Tests writing with a mocked client."""
        mocked_client = Mock()
        mocked_bucket = Mock()
        mocked_blob = Mock()
        mocked_client.bucket.return_value = mocked_bucket
        mocked_bucket.blob.return_value = mocked_blob

        data = {'key': 'value'}
        set_remaining_time(data, 'mocked-bucket', 'test.json', mocked_client)

        mocked_client.bucket.assert_called_once_with('mocked-bucket')
        mocked_bucket.blob.assert_called_once_with('test.json')
        mocked_blob.upload_from_string.assert_called_once_with(json.dumps(data), content_type='application/json')

if __name__ == '__main__':
    unittest.main()

