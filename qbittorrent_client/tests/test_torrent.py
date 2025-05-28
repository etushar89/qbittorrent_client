#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for the Torrent class.
"""

import unittest

from qbittorrent_client.torrent import Torrent


class TestTorrent(unittest.TestCase):
    """Test case for the Torrent class."""

    def setUp(self):
        """Set up the test environment."""
        # Create a sample torrent data dictionary
        self.torrent_data = {
            "hash": "abcdef1234567890",
            "name": "Test Torrent",
            "size": 1073741824,  # 1 GB
            "progress": 0.75,
            "dlspeed": 1048576,  # 1 MB/s
            "upspeed": 524288,  # 512 KB/s
            "num_seeds": 5,
            "num_leechs": 10,
            "state": "downloading",
            "eta": 3600,  # 1 hour
            "category": "test",
            "tags": "test,example",
            "added_on": 1621698000,  # Example timestamp
            "completion_on": 0,
        }
        self.torrent = Torrent(self.torrent_data)

    def test_initialization(self):
        """Test that torrent initializes correctly."""
        self.assertEqual(self.torrent.hash, "abcdef1234567890")
        self.assertEqual(self.torrent.name, "Test Torrent")
        self.assertEqual(self.torrent.size, 1073741824)
        self.assertEqual(self.torrent.progress, 0.75)
        self.assertEqual(self.torrent.state, "downloading")
        self.assertEqual(self.torrent.tags, "test,example")

    def test_progress_percent(self):
        """Test the progress_percent property."""
        self.assertEqual(self.torrent.progress_percent, 75.0)

    def test_is_downloading(self):
        """Test the is_downloading property."""
        self.assertTrue(self.torrent.is_downloading)

        # Test with different states
        self.torrent.state = "uploading"
        self.assertFalse(self.torrent.is_downloading)

    def test_is_complete(self):
        """Test the is_complete property."""
        self.assertFalse(self.torrent.is_complete)

        # Test with complete progress
        self.torrent.progress = 1.0
        self.assertTrue(self.torrent.is_complete)

    def test_is_paused(self):
        """Test the is_paused property."""
        self.assertFalse(self.torrent.is_paused)

        # Test with paused state
        self.torrent.state = "pausedDL"
        self.assertTrue(self.torrent.is_paused)

    def test_formatted_properties(self):
        """Test the formatted properties."""
        self.assertEqual(self.torrent.size_formatted, "1.00 GB")
        self.assertEqual(self.torrent.download_speed_formatted, "1.00 MB/s")
        self.assertEqual(self.torrent.upload_speed_formatted, "512.00 KB/s")
        self.assertEqual(self.torrent.eta_formatted, "1h 00m")

    def test_string_representation(self):
        """Test the string representation of the torrent."""
        expected_start = "Test Torrent - 75.0% - 1.00 GB"
        self.assertTrue(str(self.torrent).startswith(expected_start))

    def test_rename_method(self):
        """Test the rename method."""
        # Create a mock client with a rename_torrent method
        mock_client = unittest.mock.Mock()
        mock_client.rename_torrent.return_value = True

        # Rename the torrent
        result = self.torrent.rename(mock_client, "New Torrent Name")

        # Check that the client method was called with the right parameters
        mock_client.rename_torrent.assert_called_once_with(self.torrent.hash, "New Torrent Name")

        # Check that the rename operation was successful
        self.assertTrue(result)

        # Check that the torrent name was updated
        self.assertEqual(self.torrent.name, "New Torrent Name")


if __name__ == "__main__":
    unittest.main()
