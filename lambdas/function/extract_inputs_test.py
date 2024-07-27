import unittest
from unittest.mock import Mock

from main import extract_inputs, sanitise_name, sanitise_number, sanitise_time

class TestTimerFunctions(unittest.TestCase):

  # Sample data
  tournament = "Aug-2024"
  round = "Round 3"
  finish_time = "2024-08-15T12:00:00"
  time_remaining = "350"
  metadata = '{"message" : "Last round for rebuys"}'
  json_payload = {
    "tournament": tournament,
    "round": round,
    "finish_time": finish_time,
    "time_remaining": time_remaining,
    "metadata": metadata,
  }


  def test_all_inputs_present(self):
    """Tests all parameters passed in."""
    # Arrange
    request = Mock()
    request.get_json.return_value = self.json_payload
    request.args = None
    expected_output = {
      'tournament': 'Aug2024',
      'round': 'Round3',
      'finish_time': '2024-08-15T12:00:00',
      'time_remaining': '350',
      'metadata': '{"message" : "Last round for rebuys"}',
    }

    # Act
    data = extract_inputs(request)

    # Assert
    self.assertEqual(data, expected_output)

  def test_extract_inputs_missing_tournament(self):
    """Tests missing tournament parameter."""
    # Arrange
    request = Mock()
    request.get_json.return_value = self.json_payload.copy()
    del request.get_json.return_value['tournament']
    request.args = None

    # Act & Assert
    with self.assertRaisesRegex(Exception, "You need to tell me what you are doing!"):
        extract_inputs(request)

  def test_sanitise_name_success(self):
    """Tests successful sanitization of a name."""
    # Arrange
    name = "Tournament 1"
    expected_output = "Tournament1"

    # Act
    data = sanitise_name(name)

    # Assert
    self.assertEqual(data, expected_output)

  def test_sanitise_name_invalid_chars(self):
    """Tests sanitization of a name with invalid characters."""
    # Arrange
    name = "Tournament!@#$%^&*()_+=-`~|}{[]\:;?><,./"
    expected_output = "Tournament"

    # Act
    data = sanitise_name(name)

    # Assert
    self.assertEqual(data, expected_output)

  def test_sanitise_name_too_long(self):
    """Tests sanitization of a name that is too long."""
    # Arrange
    name = "a" * 256
    expected_output = "a" * 255

    # Act
    data = sanitise_name(name)

    # Assert
    self.assertEqual(data, expected_output)

  def test_sanitise_number_success(self):
    """Tests successful sanitization of a number."""
    # Arrange
    number = "12345"
    expected_output = "12345"

    # Act
    data = sanitise_number(number)

    # Assert
    self.assertEqual(data, expected_output)

  def test_sanitise_number_invalid_chars(self):
    """Tests sanitization of a number with invalid characters."""
    # Arrange
    number = "123abc45"
    expected_output = "12345"

    # Act
    data = sanitise_number(number)

    # Assert
    self.assertEqual(data, expected_output)

  def test_sanitise_number_too_long(self):
    """Tests sanitization of a number that is too long."""
    # Arrange
    number = "1" * 256
    expected_output = "1" * 255

    # Act
    data = sanitise_number(number)

    # Assert
    self.assertEqual(data, expected_output)

  def test_sanitise_time_success(self):
    """Tests successful sanitization of a time."""
    # Arrange
    time = "2024-08-15T12:00:00Z"
    expected_output = "2024-08-15T12:00:00"

    # Act
    data = sanitise_time(time)

    # Assert
    self.assertEqual(data, expected_output)

  def test_sanitise_time_invalid_format(self):
    """Tests sanitization of a time with an invalid format."""
    # Arrange
    time = "2024/08/15 12:00:00"

    # Act & Assert
    with self.assertRaises(ValueError):
      sanitise_time(time)

if __name__ == "__main__":
  unittest.main()
