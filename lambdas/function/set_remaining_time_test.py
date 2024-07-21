import json
import unittest
from unittest.mock import Mock

from set_remaining_time import set_remaining_time

class TestSetRemainingTime(unittest.TestCase):
    # sample data
    tournament="Aug2024"
    round="Round 3"
    finish_time="midnight"
    time_remaining="treefidy"

    @unittest.mock.patch("set_remaining_time.storage.Client")
    def test_write_json_to_bucket_with_mocked_client(self, mock_client):
        """Tests writing with a mocked client."""
        mocked_bucket = Mock()
        mocked_blob = Mock()
        mock_client.bucket.return_value = mocked_bucket
        mocked_bucket.blob.return_value = mocked_blob


        data = set_remaining_time(tournament=self.tournament, round=self.round, finish_time=self.finish_time, time_remaining=self.time_remaining, storage_client=mock_client)

        expected_output = f'{{"round": "{self.round}", "finish_time": "{self.finish_time}", "time_remaining": "{self.time_remaining}"}}'
        mock_client.bucket.assert_called_once_with("bpt")
        mocked_bucket.blob.assert_called_once_with("Aug2024")
        mocked_blob.upload_from_string.assert_called_once_with(data=expected_output, content_type="application/json")
        self.assertEqual(data, expected_output)

    @unittest.mock.patch("set_remaining_time.storage.Client")
    def test_download_error(self, mock_client):
        """Tests error handling during download."""
        mocked_blob = Mock()
        mocked_blob.upload_from_string.side_effect=Exception("testing download error")
        mocked_bucket = Mock()
        mocked_bucket.blob.return_value = mocked_blob
        mock_client.bucket.return_value = mocked_bucket

        data = set_remaining_time(tournament=self.tournament, round=self.round, finish_time=self.finish_time, time_remaining=self.time_remaining, storage_client=mock_client)

        expected_output = '{"error": "testing download error"}'
        self.assertEqual(data, expected_output)

if __name__ == "__main__":
    unittest.main()

