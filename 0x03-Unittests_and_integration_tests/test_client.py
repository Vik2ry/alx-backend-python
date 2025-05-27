#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class.

This module contains test cases for the GithubOrgClient class, using
unittest and mock to verify its behavior. The tests cover:
- Fetching organization data from the GitHub API.
- Retrieving the public repositories URL from the organization data.
- Listing public repositories and verifying their names.
- Checking if a repository has a specific license.

Tested methods include:
- org property: Ensures correct API call and data retrieval.
- _public_repos_url property: Ensures correct extraction of repos_url.
- public_repos method: Ensures correct listing of repository names.
- has_license static method: Ensures correct license key checking.

Mocks are used to isolate external dependencies and API calls.
"""

from fixtures import TEST_PAYLOAD
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized_class, parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct org data and
        calls get_json with the right URL.
        """
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct repos_url.
        """
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the correct list of repo names.
        """
        payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}}
        ]
        mock_get_json.return_value = payload
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://test-url"
            client = GithubOrgClient("test")
            self.assertEqual(
                client.public_repos(),
                ["repo1", "repo2"]
            )
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://test-url")

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns True if repo has the given license.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": org,
        "repos_payload": repos,
        "expected_repos": expected,
        "apache2_repos": apache2
    } for org, repos, expected, apache2 in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos with HTTP calls mocked.
    """

    @classmethod
    def setUpClass(cls):
        """
        Start patching requests.get with JSON payloads from fixtures.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Setup .json() return values in order of usage: org -> repos
        cls.mock_get.return_value = MagicMock()
        cls.mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
            cls.org_payload,
            cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """
        Stop patching requests.get.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos returns expected repo names.
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self):
        """
        Test public_repos returns filtered repos by license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
