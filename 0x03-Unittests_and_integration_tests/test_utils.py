#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        test_url = "http://example.com"
        test_payload = {"payload": True}
        mock_get.return_value.json.return_value = test_payload

        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=99) as mock_method:
            self.assertEqual(test_obj.a_property, 42)
            self.assertEqual(test_obj.a_property, 42)
            mock_method.assert_not_called()


if __name__ == '__main__':
    unittest.main()
