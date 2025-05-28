#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Credentials Manager Module

This module provides utilities for securely storing and retrieving
qBittorrent credentials.
"""

import base64
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple


class CredentialsManager:
    """
    A class for managing qBittorrent WebUI credentials.

    This class provides methods for securely storing and retrieving
    qBittorrent WebUI credentials.
    """

    def __init__(self):
        """Initialize the CredentialsManager."""
        self.logger = logging.getLogger("qbittorrent_client.credentials")
        self.temp_dir = tempfile.gettempdir()
        self.credentials_file = Path(self.temp_dir) / ".qbittorrent_credentials"

    def save_credentials(self, url: str, username: str, password: str) -> bool:
        """
        Save credentials to a temporary file.

        Args:
            url: The qBittorrent WebUI URL
            username: The username for qBittorrent WebUI
            password: The password for qBittorrent WebUI

        Returns:
            bool: True if credentials were saved successfully, False otherwise
        """
        try:
            # Simple encoding (not encryption) to avoid plain text passwords
            # This is not fully secure but better than plaintext
            encoded_password = base64.b64encode(password.encode()).decode()

            credentials = {"url": url, "username": username, "password": encoded_password}

            # Create a temp file with restricted permissions
            with open(self.credentials_file, "w", encoding="utf-8") as f:
                json.dump(credentials, f)

            # Set file permissions to restrict access to only the current user
            os.chmod(self.credentials_file, 0o600)

            self.logger.info(f"Credentials saved to {self.credentials_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save credentials: {e}")
            return False

    def get_credentials(self, url: str = None) -> Optional[Dict[str, str]]:
        """
        Get credentials from the temporary file.

        Args:
            url: The qBittorrent WebUI URL to match (if None, return any saved credentials)        Returns:
            Optional[Dict[str, str]]: A dictionary containing the credentials if found,
                                      None otherwise
        """
        if not self.credentials_file.exists():
            self.logger.debug("Credentials file not found")
            return None

        try:
            with open(self.credentials_file, "r", encoding="utf-8") as f:
                credentials = json.load(f)

            # If URL is provided, only return credentials for that URL
            if url and credentials.get("url") != url:
                self.logger.debug(f"No credentials found for URL: {url}")
                return None

            # Decode the password
            if "password" in credentials:
                credentials["password"] = base64.b64decode(
                    credentials["password"].encode()
                ).decode()

            return credentials

        except Exception as e:
            self.logger.error(f"Failed to retrieve credentials: {e}")
            return None

    def clear_credentials(self) -> bool:
        """
        Clear saved credentials.

        Returns:
            bool: True if credentials were cleared successfully, False otherwise
        """
        try:
            if self.credentials_file.exists():
                self.credentials_file.unlink()
                self.logger.info("Credentials cleared")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to clear credentials: {e}")
            return False

    def get_url_username_password(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Tuple[str, str, str]:
        """
        Get the URL, username, and password, using cached credentials if available.

        Args:
            url: The qBittorrent WebUI URL (optional)
            username: The username for qBittorrent WebUI (optional)
            password: The password for qBittorrent WebUI (optional)

        Returns:
            Tuple[str, str, str]: The URL, username, and password
        """
        # Try to get cached credentials for the specific URL if provided
        cached_credentials = None
        if url:
            cached_credentials = self.get_credentials(url)

        # If no credentials for this specific URL, try to get any cached credentials
        if not cached_credentials:
            cached_credentials = self.get_credentials()

        # Use provided values or fall back to cached values
        final_url = url or (
            cached_credentials.get("url") if cached_credentials else "http://localhost:8080"
        )
        final_username = username or (
            cached_credentials.get("username") if cached_credentials else None
        )
        final_password = password or (
            cached_credentials.get("password") if cached_credentials else None
        )

        return final_url, final_username, final_password
