#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for the QBittorrentClient class.
"""

import unittest
from unittest.mock import Mock, patch

from qbittorrent_client.qbittorrent_client import QBittorrentAPIError, QBittorrentClient


class TestQBittorrentClient(unittest.TestCase):
    """Test case for the QBittorrentClient class."""

    def setUp(self):
        """Set up the test environment."""
        # Use patch to prevent actual sessions from being created during initialization
        patcher = patch("qbittorrent_client.qbittorrent_client.requests.Session")
        self.mock_session = patcher.start()
        self.addCleanup(patcher.stop)
        
        # Configure the mock session
        self.session_instance = Mock()
        self.mock_session.return_value = self.session_instance
        
        self.client = QBittorrentClient("http://localhost:8080")

    def test_initialization(self):
        """Test that client initializes correctly."""
        self.assertEqual(self.client.base_url, "http://localhost:8080/")
        self.assertEqual(self.client.api_url, "http://localhost:8080/api/v2/")
        self.assertFalse(self.client.is_authenticated)

    def test_login_success(self):
        """Test successful login."""
        # Setup mock response
        mock_response = Mock()
        mock_response.cookies = {"SID": "test_sid"}
        mock_response.raise_for_status.return_value = None
        self.session_instance.request.return_value = mock_response

        # Call login
        result = self.client.login("username", "password")

        # Check assertions
        self.assertTrue(result)
        self.assertTrue(self.client.is_authenticated)
        self.session_instance.request.assert_called_once()

    def test_login_failure(self):
        """Test login failure."""
        # Setup mock response
        mock_response = Mock()
        mock_response.cookies = {}
        mock_response.raise_for_status.return_value = None
        self.session_instance.request.return_value = mock_response

        # Call login
        result = self.client.login("username", "password")

        # Check assertions
        self.assertFalse(result)
        self.assertFalse(self.client.is_authenticated)

    def test_get_api_version(self):
        """Test getting API version."""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = "2.0"
        mock_response.raise_for_status.return_value = None
        self.session_instance.request.return_value = mock_response

        # Call method
        version = self.client.get_api_version()

        # Check assertions
        self.assertEqual(version, "2.0")
        
    def test_rename_torrent_success(self):
        """Test successful torrent rename."""
        # Setup authentication
        self.client.is_authenticated = True
        
        # Setup mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        self.session_instance.request.return_value = mock_response

        # Call method
        result = self.client.rename_torrent("test_hash", "New Name")

        # Check assertions
        self.assertTrue(result)
        self.session_instance.request.assert_called_with(
            method="POST",
            url="http://localhost:8080/api/v2/torrents/rename",
            params=None,
            data={"hash": "test_hash", "name": "New Name"},
            files=None,
            headers={"Referer": "http://localhost:8080/"}
        )

    def test_rename_torrent_not_authenticated(self):
        """Test rename torrent failure when not authenticated."""
        # Ensure not authenticated
        self.client.is_authenticated = False

        # Check that it raises the expected exception
        with self.assertRaises(QBittorrentAPIError) as context:
            self.client.rename_torrent("test_hash", "New Name")

        # Verify error message
        self.assertIn("Not authenticated", str(context.exception))


if __name__ == "__main__":
    unittest.main()
