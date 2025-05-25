#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QBittorrent Client Example

This script demonstrates how to use the qBittorrent client to authenticate
and retrieve a list of torrents.
"""

import argparse
import getpass
import os
import sys
from typing import Dict, List

from qbittorrent_client import (
    CredentialsManager,
    QBittorrentAPIError,
    QBittorrentClient,
    Torrent,
)


def display_torrent_info(torrent: Torrent) -> None:
    """
    Display information about a torrent.

    Args:
        torrent: The torrent to display information for.
    """
    progress = f"{torrent.progress_percent:.1f}%"

    print(f"Name: {torrent.name}")
    print(f"Hash: {torrent.hash}")
    print(f"Size: {torrent.size_formatted}")
    print(f"Progress: {progress}")
    print(f"State: {torrent.state}")
    print(f"Download Speed: {torrent.download_speed_formatted}")
    print(f"Upload Speed: {torrent.upload_speed_formatted}")
    print(f"ETA: {torrent.eta_formatted}")
    print(f"Seeds/Peers: {torrent.num_seeds}/{torrent.num_leechs}")
    print("-" * 50)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="QBittorrent Client Example")

    parser.add_argument(
        "--url",
        default="http://localhost:8080",
        help="QBittorrent WebUI URL (default: http://localhost:8080)",
    )

    parser.add_argument("--username", help="QBittorrent WebUI username")

    parser.add_argument(
        "--password", help="QBittorrent WebUI password (will prompt if not provided)"
    )

    parser.add_argument("--cache", action="store_true", help="Cache credentials for future use")

    parser.add_argument("--clear-cache", action="store_true", help="Clear cached credentials")

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the example.
    """
    args = parse_arguments()

    # Initialize credentials manager
    credentials_manager = CredentialsManager()

    if args.clear_cache:
        if credentials_manager.clear_credentials():
            print("Cached credentials cleared successfully.")
        else:
            print("No cached credentials found.")
        return

    # Try to get credentials from cache or command line
    url, username, password = credentials_manager.get_url_username_password(
        args.url, args.username, args.password
    )

    # If username is still not available, prompt for it
    if not username:
        username = input("Username: ")

    # If password is still not available, prompt for it
    if not password:
        password = getpass.getpass("Password: ")

    # Create the client
    client = QBittorrentClient(url)

    try:
        # Login to the client
        client.login(username, password)
        print("Login successful!")

        # Save credentials if requested
        if args.cache:
            if credentials_manager.save_credentials(url, username, password):
                print("Credentials cached for future use.")
            else:
                print("Failed to cache credentials.")

        # Get qBittorrent version information
        api_version = client.get_api_version()
        app_version = client.get_app_version()
        print(f"qBittorrent version: {app_version}")
        print(f"API version: {api_version}")

        # Get torrents
        print("\nRetrieving torrents...")
        torrents_data = client.get_torrents()

        # Create Torrent objects from raw data
        torrents = [Torrent(data) for data in torrents_data]

        # Display torrent information
        if not torrents:
            print("No torrents found.")
        else:
            print(f"\nFound {len(torrents)} torrents:\n")
            for i, torrent in enumerate(torrents, 1):
                print(f"Torrent {i}:")
                display_torrent_info(torrent)

        # Logout
        client.logout()
        print("Logged out successfully.")

    except QBittorrentAPIError as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
