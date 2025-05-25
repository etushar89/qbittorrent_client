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
        self.client = QBittorrentClient("http://localhost:8080")

    def test_initialization(self):
        """Test that client initializes correctly."""
        self.assertEqual(self.client.base_url, "http://localhost:8080/")
        self.assertEqual(self.client.api_url, "http://localhost:8080/api/v2/")
        self.assertFalse(self.client.is_authenticated)

    @patch("qbittorrent_client.qbittorrent_client.requests.Session")
    def test_login_success(self, mock_session):
        """Test successful login."""
        # Setup mock response
        mock_response = Mock()
        mock_response.cookies = {"SID": "test_sid"}
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_response

        # Call login
        result = self.client.login("username", "password")

        # Check assertions
        self.assertTrue(result)
        self.assertTrue(self.client.is_authenticated)
        mock_session.return_value.request.assert_called_once()

    @patch("qbittorrent_client.qbittorrent_client.requests.Session")
    def test_login_failure(self, mock_session):
        """Test login failure."""
        # Setup mock response
        mock_response = Mock()
        mock_response.cookies = {}
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_response

        # Call login
        result = self.client.login("username", "password")

        # Check assertions
        self.assertFalse(result)
        self.assertFalse(self.client.is_authenticated)

    @patch("qbittorrent_client.qbittorrent_client.requests.Session")
    def test_get_api_version(self, mock_session):
        """Test getting API version."""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = "2.0"
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_response

        # Call method
        version = self.client.get_api_version()

        # Check assertions
        self.assertEqual(version, "2.0")


if __name__ == "__main__":
    unittest.main()
