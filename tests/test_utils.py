import unittest
from unittest.mock import patch

from src.utils import load_transactions


class TestUtils(unittest.TestCase):

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_open):
        result = load_transactions("non_existent.json")
        self.assertEqual(result, [])
