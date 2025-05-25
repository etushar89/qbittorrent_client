"""
QBittorrent Client Package

This package provides a Python client for interacting with the qBittorrent Web API.
"""

from .qbittorrent_client import QBittorrentClient, QBittorrentAPIError
from .torrent import Torrent
from .credentials import CredentialsManager

__version__ = "0.1.0"
__all__ = ["QBittorrentClient", "QBittorrentAPIError", "Torrent", "CredentialsManager"]
