#!/usr/bin/env python3
"""
Unit tests for utility functions in the utils module.

This module contains unit tests for the following functions:
    - access_nested_map
    - get_json
    - memoize

Each test class is responsible for testing a specific function.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the `access_nested_map` utility function.

    This class uses parameterized tests to verify the correct behavior of
    the `access_nested_map` function. The tests cover both successful
    access of nested mappings and the correct raising of `KeyError`
    exceptions when keys are missing.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected value for valid paths.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """
        Test that access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_msg}'")


class TestGetJson(unittest.TestCase):
    """
    Unit tests for the `get_json` utility function.

    This class tests that get_json returns the expected payload and that
    requests.get is called with the correct URL.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns the correct JSON payload from a URL.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Unit tests for the `memoize` utility decorator.

    This class tests that memoize caches the result of a method.
    """

    def test_memoize(self):
        """
        Test that memoize caches the result of a method.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_mtd:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_mtd.assert_called_once()


if __name__ == '__main__':
    unittest.main()
