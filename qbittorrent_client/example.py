#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QBittorrent Client Example

This script demonstrates how to use the qBittorrent client to authenticate
and retrieve a list of torrents.
"""

import argparse
import getpass
import sys

from credentials import CredentialsManager
from torrent import Torrent

from qbittorrent_client import (
    QBittorrentAPIError,
    QBittorrentClient,
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

    parser.add_argument(
        "--rename",
        nargs=2,
        metavar=("HASH", "NAME"),
        help="Rename a torrent with the specified hash to the new name",
    )

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
        return  # Try to get credentials from cache or command line
    url, username, password = credentials_manager.get_url_username_password(
        args.url, args.username, args.password
    )

    # If username is still not available, prompt for it
    if not username:
        username = input("Username: ")

    # If password is still not available, prompt for it
    if not password:
        password = getpass.getpass("Password: ")

    # Handle the rename argument separately if provided
    rename_hash = None
    rename_name = None
    if args.rename:
        rename_hash, rename_name = args.rename

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
                print("Failed to cache credentials.")  # Get qBittorrent version information
        api_version = client.get_api_version()
        app_version = client.get_app_version()
        print(f"qBittorrent version: {app_version}")
        print(f"API version: {api_version}")

        # Handle torrent rename if requested via command line
        if rename_hash and rename_name:
            try:
                client.rename_torrent(rename_hash, rename_name)
                print(f"Successfully renamed torrent with hash '{rename_hash}' to '{rename_name}'")
            except QBittorrentAPIError as error:
                print(f"Failed to rename torrent: {error}")

        # Get torrents
        print("\nRetrieving torrents...")
        torrents_data = client.get_torrents()

        # Create Torrent objects from raw data
        torrents = [Torrent(data) for data in torrents_data]  # Display torrent information
        if not torrents:
            print("No torrents found.")
        else:
            print(f"\nFound {len(torrents)} torrents:\n")
            for i, torrent in enumerate(torrents, 1):
                print(f"Torrent {i}:")
                display_torrent_info(torrent)
            # Demonstrate renaming functionality for the first torrent
            if (
                torrents
                and input("\nDo you want to rename the first torrent? (y/n): ").lower() == "y"
            ):
                first_torrent = torrents[0]
                new_name = input(f"Enter new name for '{first_torrent.name}': ")
                if new_name:
                    try:
                        # Using the Torrent.rename method
                        first_torrent.rename(client, new_name)
                        print(f"Successfully renamed torrent to '{new_name}'")
                    except QBittorrentAPIError as error:
                        print(f"Failed to rename torrent: {error}")

        # Logout
        client.logout()
        print("Logged out successfully.")

    except QBittorrentAPIError as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
