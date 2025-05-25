#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Torrent Module

This module provides the Torrent class for representing qBittorrent torrents.
"""

from datetime import datetime
from typing import Dict, Any


class Torrent:
    """
    A class representing a torrent in qBittorrent.

    This class encapsulates the properties of a torrent and provides
    utility methods for working with torrent data.
    """

    def __init__(self, torrent_data: Dict[str, Any]):
        """
        Initialize a Torrent object with data from the qBittorrent API.

        Args:
            torrent_data: A dictionary containing torrent data from the API.
        """
        self.hash = torrent_data.get("hash", "")
        self.name = torrent_data.get("name", "")
        self.size = torrent_data.get("size", 0)
        self.progress = torrent_data.get("progress", 0.0)
        self.dlspeed = torrent_data.get("dlspeed", 0)
        self.upspeed = torrent_data.get("upspeed", 0)
        self.num_seeds = torrent_data.get("num_seeds", 0)
        self.num_leechs = torrent_data.get("num_leechs", 0)
        self.state = torrent_data.get("state", "")
        self.eta = torrent_data.get("eta", 0)
        self.category = torrent_data.get("category", "")
        self.tags = torrent_data.get("tags", "")

        # Convert timestamps to datetime objects
        self.added_on = datetime.fromtimestamp(torrent_data.get("added_on", 0))
        self.completion_on = (
            datetime.fromtimestamp(torrent_data.get("completion_on", 0))
            if torrent_data.get("completion_on", 0) > 0
            else None
        )

        # Store the original data
        self._raw_data = torrent_data

    @property
    def progress_percent(self) -> float:
        """
        Get the progress as a percentage.

        Returns:
            float: The torrent progress as a percentage (0-100).
        """
        return self.progress * 100

    @property
    def is_complete(self) -> bool:
        """
        Check if the torrent is complete.

        Returns:
            bool: True if the torrent is complete.
        """
        return self.progress >= 0.999

    @property
    def is_downloading(self) -> bool:
        """
        Check if the torrent is currently downloading.

        Returns:
            bool: True if the torrent is in a downloading state.
        """
        return self.state in ("downloading", "stalledDL", "metaDL", "forcedDL")

    @property
    def is_uploading(self) -> bool:
        """
        Check if the torrent is currently uploading/seeding.

        Returns:
            bool: True if the torrent is in an uploading/seeding state.
        """
        return self.state in ("uploading", "stalledUP", "forcedUP")

    @property
    def is_paused(self) -> bool:
        """
        Check if the torrent is paused.

        Returns:
            bool: True if the torrent is paused.
        """
        return self.state in ("pausedDL", "pausedUP")

    @property
    def download_speed_formatted(self) -> str:
        """
        Get the download speed in a human-readable format.

        Returns:
            str: The formatted download speed.
        """
        return self._format_speed(self.dlspeed)

    @property
    def upload_speed_formatted(self) -> str:
        """
        Get the upload speed in a human-readable format.

        Returns:
            str: The formatted upload speed.
        """
        return self._format_speed(self.upspeed)

    @property
    def size_formatted(self) -> str:
        """
        Get the torrent size in a human-readable format.

        Returns:
            str: The formatted size.
        """
        return self._format_size(self.size)

    @property
    def eta_formatted(self) -> str:
        """
        Get the ETA in a human-readable format.

        Returns:
            str: The formatted ETA.
        """
        if self.eta <= 0 or self.eta >= 8640000:  # Invalid or >100 days
            return "∞"

        seconds = self.eta
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days}d {hours:02d}h"
        elif hours > 0:
            return f"{hours}h {minutes:02d}m"
        else:
            return f"{minutes}m {seconds:02d}s"

    def _format_size(self, size_bytes: int) -> str:
        """
        Format a byte size into a human-readable string.

        Args:
            size_bytes: The size in bytes.

        Returns:
            str: The formatted size string.
        """
        if size_bytes == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = float(size_bytes)
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.2f} {units[unit_index]}"

    def _format_speed(self, speed_bytes: int) -> str:
        """
        Format a byte speed into a human-readable string.

        Args:
            speed_bytes: The speed in bytes per second.

        Returns:
            str: The formatted speed string.
        """
        if speed_bytes == 0:
            return "0 B/s"

        return f"{self._format_size(speed_bytes)}/s"

    def __str__(self) -> str:
        """
        Return a string representation of the torrent.

        Returns:
            str: A string with the torrent's basic information.
        """
        return (
            f"{self.name} - {self.progress_percent:.1f}% - {self.size_formatted} - "
            f"DL: {self.download_speed_formatted} - UL: {self.upload_speed_formatted} - "
            f"State: {self.state}"
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the torrent for debugging.

        Returns:
            str: A string with the torrent's class name and hash.
        """
        return f"<Torrent {self.hash}: {self.name}>"
