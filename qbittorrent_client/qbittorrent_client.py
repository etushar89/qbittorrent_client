#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QBittorrent Client Module

This module provides a Python client for the qBittorrent Web API.
It allows for authentication and interaction with torrents.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urljoin


class QBittorrentAPIError(Exception):
    """Exception raised for errors in the QBittorrent API."""

    pass


class QBittorrentClient:
    """
    A client for interacting with the qBittorrent Web API.

    This class provides methods to authenticate with the qBittorrent Web API
    and perform operations such as retrieving torrent information.
    """

    def __init__(self, base_url: str = "http://localhost:8080/"):
        """
        Initialize the QBittorrent client.

        Args:
            base_url: The base URL of the qBittorrent Web API.
                      Defaults to 'http://localhost:8080/'.
        """
        self.base_url = base_url if base_url.endswith("/") else f"{base_url}/"
        self.session = requests.Session()
        self.api_url = urljoin(self.base_url, "api/v2/")
        self.is_authenticated = False
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up a logger for the client.

        Returns:
            logging.Logger: A configured logger instance.
        """
        logger = logging.getLogger("qbittorrent_client")
        logger.setLevel(logging.INFO)

        # Add handler if none exists
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ) -> requests.Response:
        """
        Make a request to the qBittorrent Web API.

        Args:
            endpoint: The API endpoint to call.
            method: The HTTP method to use (GET, POST, etc).
            params: URL parameters to include in the request.
            data: Form data to include in the request.
            files: Files to upload.

        Returns:
            requests.Response: The response from the API.

        Raises:
            QBittorrentAPIError: If the request fails or returns an error.
        """
        url = urljoin(self.api_url, endpoint)
        self.logger.debug(f"Making {method} request to {url}")

        headers = {"Referer": self.base_url}

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                files=files,
                headers=headers,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Request failed: {error}")
            message = f"API request failed: {error}"

            # Try to get more detailed error information
            try:
                error_details = response.json()
                message += f" - Details: {error_details}"
            except (ValueError, AttributeError):
                if response is not None and response.text:
                    message += f" - Response: {response.text}"

            raise QBittorrentAPIError(message) from error

    def login(self, username: str, password: str) -> bool:
        """
        Log in to the qBittorrent Web UI.

        Args:
            username: The username to use for authentication.
            password: The password to use for authentication.

        Returns:
            bool: True if authentication was successful.

        Raises:
            QBittorrentAPIError: If authentication fails.
        """
        self.logger.info("Attempting to log in to qBittorrent Web UI")

        data = {"username": username, "password": password}

        try:
            response = self._make_request("auth/login", method="POST", data=data)

            # The API returns OK (200) with a cookie on successful login
            if response.cookies:
                self.is_authenticated = True
                self.logger.info("Successfully logged in to qBittorrent Web UI")
                return True
            else:
                self.logger.warning("Login successful but no session cookie received")
                self.is_authenticated = False
                return False

        except QBittorrentAPIError as error:
            self.logger.error(f"Login failed: {error}")
            self.is_authenticated = False
            raise

    def logout(self) -> bool:
        """
        Log out from the qBittorrent Web UI.

        Returns:
            bool: True if logout was successful.

        Raises:
            QBittorrentAPIError: If logout fails.
        """
        self.logger.info("Logging out from qBittorrent Web UI")

        try:
            self._make_request("auth/logout", method="POST")
            self.is_authenticated = False
            self.logger.info("Successfully logged out from qBittorrent Web UI")
            return True

        except QBittorrentAPIError as error:
            self.logger.error(f"Logout failed: {error}")
            raise

    def get_torrents(self, filter_status: str = "all", **kwargs) -> List[Dict]:
        """
        Get the list of torrents.

        Args:
            filter_status: Filter torrents by status (all, downloading, seeding, etc.).
            **kwargs: Additional filtering parameters (category, sort, limit, etc.).

        Returns:
            List[Dict]: A list of dictionaries containing torrent information.

        Raises:
            QBittorrentAPIError: If the request fails or if not authenticated.
        """
        if not self.is_authenticated:
            self.logger.error("Not authenticated. Please log in first.")
            raise QBittorrentAPIError("Not authenticated. Please log in first.")

        self.logger.info(f"Getting torrents with filter: {filter_status}")

        params = {"filter": filter_status}

        # Add additional parameters if provided
        if kwargs:
            params.update(kwargs)

        try:
            response = self._make_request("torrents/info", params=params)
            torrents = response.json()

            self.logger.info(f"Retrieved {len(torrents)} torrents")
            return torrents

        except QBittorrentAPIError as error:
            self.logger.error(f"Failed to get torrents: {error}")
            raise

    def get_torrent_properties(self, torrent_hash: str) -> Dict:
        """
        Get properties of a specific torrent.

        Args:
            torrent_hash: The hash of the torrent to get properties for.

        Returns:
            Dict: A dictionary containing the torrent's properties.

        Raises:
            QBittorrentAPIError: If the request fails or if not authenticated.
        """
        if not self.is_authenticated:
            self.logger.error("Not authenticated. Please log in first.")
            raise QBittorrentAPIError("Not authenticated. Please log in first.")

        self.logger.info(f"Getting properties for torrent with hash: {torrent_hash}")

        params = {"hash": torrent_hash}

        try:
            response = self._make_request("torrents/properties", params=params)
            properties = response.json()

            self.logger.info(f"Retrieved properties for torrent: {torrent_hash}")
            return properties

        except QBittorrentAPIError as error:
            self.logger.error(f"Failed to get torrent properties: {error}")
            raise

    def get_app_version(self) -> str:
        """
        Get the qBittorrent application version.

        Returns:
            str: The qBittorrent application version.

        Raises:
            QBittorrentAPIError: If the request fails.
        """
        try:
            response = self._make_request("app/version")
            version = response.text.strip()

            self.logger.info(f"qBittorrent version: {version}")
            return version

        except QBittorrentAPIError as error:
            self.logger.error(f"Failed to get application version: {error}")
            raise

    def get_api_version(self) -> str:
        """
        Get the qBittorrent Web API version.

        Returns:
            str: The qBittorrent Web API version.

        Raises:
            QBittorrentAPIError: If the request fails.
        """
        try:
            response = self._make_request("app/webapiVersion")
            version = response.text.strip()

            self.logger.info(f"qBittorrent Web API version: {version}")
            return version

        except QBittorrentAPIError as error:
            self.logger.error(f"Failed to get API version: {error}")
            raise
