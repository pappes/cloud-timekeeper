import flask
import unittest
from unittest.mock import Mock

from set_remaining_time import set_remaining_time

class TestSetRemainingTime(unittest.TestCase):
    # sample data
    tournament="Aug2024"
    round="Round 3"
    finish_time="midnight"
    time_remaining="treefidy"

    @unittest.mock.patch("set_remaining_time.abort")
    def test_write_json_to_bucket_with_mocked_client(self, mock_abort):
        """Tests writing with a mocked client."""
        # Arrange.
        mocked_bucket = Mock()
        mocked_blob = Mock()
        mocked_client = Mock()
        mocked_client.bucket.return_value = mocked_bucket
        mocked_bucket.blob.return_value = mocked_blob
        mocked_blob.upload_from_string.return_value = 'mocked_blob'
        request = Mock()
        request.get_json.return_value = {
            "tournament": self.tournament,
            "round": self.round,
            "finish_time": self.finish_time,
            "time_remaining": self.time_remaining
        }
        request.args = None

        expected_output = f'{{"round": "{self.round}", "finish_time": "{self.finish_time}", "time_remaining": "{self.time_remaining}"}}'

        # Act.
        data = set_remaining_time(request, storage_client=mocked_client)

        # Assert.
        mocked_client.bucket.assert_called_once_with("bpt-timer")
        mocked_bucket.blob.assert_called_once_with("Aug2024")
        mocked_blob.upload_from_string.assert_called_once_with(data=expected_output, content_type="application/json")
        self.assertEqual(data, expected_output)

    @unittest.mock.patch("set_remaining_time.abort")
    def test_download_error(self, mock_abort):
        """Tests error handling during download."""
        # Arrange.
        mocked_bucket = Mock()
        mocked_blob = Mock()
        mocked_client = Mock()
        mocked_client.bucket.return_value = mocked_bucket
        mocked_blob.upload_from_string.side_effect=Exception("testing upload error")
        request = Mock()
        request.get_json.return_value = {"tournament": "data.json"}
        request.get_json.return_value = {"round": "data.json"}
        request.get_json.return_value = {"finish_time": "data.json"}
        request.get_json.return_value = {"time_remaining": "data.json"}
        request.args = None

        expected_output = '{"error": "You need to tell me what you are doing!"}'

        # Act.
        data = set_remaining_time(request, storage_client=mocked_client)

        # Assert.
        mock_abort.assert_called_once_with(400, expected_output)
        self.assertIs(data, mock_abort())

    @unittest.mock.patch("set_remaining_time.abort")
    def test_parameter_error(self, mock_abort):
        """Tests error in invocation parameters."""
        # Arrange.
        mocked_client = Mock()
        request = Mock()
        request.get_json.return_value = None
        request.args = None

        expected_output = '{"error": "You need to tell me what you are doing!"}'

        # Act.
        data = set_remaining_time(request, storage_client=mocked_client)

        # Assert.
        mock_abort.assert_called_once_with(400, expected_output)
        self.assertIs(data, mock_abort())

if __name__ == "__main__":
    unittest.main()

