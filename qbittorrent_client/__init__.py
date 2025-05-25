"""
QBittorrent Client Package

This package provides a Python client for interacting with the qBittorrent Web API.
"""

from .credentials import CredentialsManager
from .qbittorrent_client import QBittorrentAPIError, QBittorrentClient
from .torrent import Torrent

__version__ = "0.1.0"
__all__ = ["QBittorrentClient", "QBittorrentAPIError", "Torrent", "CredentialsManager"]
