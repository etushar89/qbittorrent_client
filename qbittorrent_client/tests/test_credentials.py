#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for the CredentialsManager class.
"""

import unittest

from qbittorrent_client import CredentialsManager


class TestCredentialsManager(unittest.TestCase):
    """Test case for the CredentialsManager class."""

    def setUp(self):
        """Set up the test environment."""
        self.credentials_manager = CredentialsManager()
        # Ensure we start with no credentials
        self.credentials_manager.clear_credentials()

    def tearDown(self):
        """Tear down the test environment."""
        # Clean up after the tests
        self.credentials_manager.clear_credentials()

    def test_save_and_get_credentials(self):
        """Test saving and retrieving credentials."""
        # Save credentials
        url = "http://test.com:8080"
        username = "testuser"
        password = "testpass123"

        result = self.credentials_manager.save_credentials(url, username, password)
        self.assertTrue(result)

        # Retrieve credentials
        credentials = self.credentials_manager.get_credentials()
        self.assertIsNotNone(credentials)
        self.assertEqual(credentials["url"], url)
        self.assertEqual(credentials["username"], username)
        self.assertEqual(credentials["password"], password)

        # Retrieve with URL filter - matching
        credentials = self.credentials_manager.get_credentials(url)
        self.assertIsNotNone(credentials)

        # Retrieve with URL filter - non-matching
        credentials = self.credentials_manager.get_credentials("http://different.com")
        self.assertIsNone(credentials)

    def test_get_url_username_password(self):
        """Test the convenience method for getting URL, username and password."""
        # Save credentials
        url = "http://test.com:8080"
        username = "testuser"
        password = "testpass123"
        self.credentials_manager.save_credentials(url, username, password)

        # Get with no parameters (should use cached)
        result_url, result_username, result_password = (
            self.credentials_manager.get_url_username_password()
        )
        self.assertEqual(result_url, url)
        self.assertEqual(result_username, username)
        self.assertEqual(result_password, password)

        # Get with some parameters (should override cached)
        new_url = "http://new.com:8080"
        result_url, result_username, result_password = (
            self.credentials_manager.get_url_username_password(new_url)
        )
        self.assertEqual(result_url, new_url)
        self.assertEqual(result_username, username)
        self.assertEqual(result_password, password)

        # Get with all parameters (should override cached)
        new_username = "newuser"
        new_password = "newpass"
        result_url, result_username, result_password = (
            self.credentials_manager.get_url_username_password(new_url, new_username, new_password)
        )
        self.assertEqual(result_url, new_url)
        self.assertEqual(result_username, new_username)
        self.assertEqual(result_password, new_password)

    def test_clear_credentials(self):
        """Test clearing credentials."""
        # Save credentials
        url = "http://test.com:8080"
        username = "testuser"
        password = "testpass123"
        self.credentials_manager.save_credentials(url, username, password)

        # Verify they exist
        credentials = self.credentials_manager.get_credentials()
        self.assertIsNotNone(credentials)

        # Clear credentials
        result = self.credentials_manager.clear_credentials()
        self.assertTrue(result)

        # Verify they are gone
        credentials = self.credentials_manager.get_credentials()
        self.assertIsNone(credentials)

        # Clear again (should return False since no file exists)
        result = self.credentials_manager.clear_credentials()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
