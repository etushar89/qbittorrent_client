#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Credential Caching Example

This script demonstrates how to use the credential caching feature
of the qBittorrent client.
"""

import os
import sys
import getpass
import argparse

from qbittorrent_client import (
    QBittorrentClient,
    QBittorrentAPIError,
    CredentialsManager,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="qBittorrent Client Credential Caching Example"
    )

    parser.add_argument("--save", action="store_true", help="Save credentials")

    parser.add_argument("--clear", action="store_true", help="Clear saved credentials")

    parser.add_argument(
        "--url",
        default="http://localhost:8080",
        help="URL of the qBittorrent WebUI (default: http://localhost:8080)",
    )

    parser.add_argument("--username", help="Username for qBittorrent WebUI")

    parser.add_argument("--password", help="Password for qBittorrent WebUI")

    return parser.parse_args()


def main() -> None:
    """Main function."""
    args = parse_arguments()
    credentials_manager = CredentialsManager()

    # Handle clear request
    if args.clear:
        if credentials_manager.clear_credentials():
            print("Credentials cleared successfully.")
        else:
            print("No credentials found or failed to clear credentials.")
        return

    # Handle save request
    if args.save:
        username = args.username
        if not username:
            username = input("Username: ")

        password = args.password
        if not password:
            password = getpass.getpass("Password: ")

        if credentials_manager.save_credentials(args.url, username, password):
            print(f"Credentials for {username}@{args.url} saved successfully.")
        else:
            print("Failed to save credentials.")
        return

    # Use saved credentials to connect
    print("Attempting to use saved credentials...")
    url, username, password = credentials_manager.get_url_username_password()

    if not username or not password:
        print("No saved credentials found or incomplete credentials.")
        sys.exit(1)

    print(f"Found credentials for {username}@{url}")

    # Create client and try to login
    client = QBittorrentClient(url)
    try:
        client.login(username, password)
        print("Login successful!")

        # Get and display torrents
        torrents = client.get_torrents()
        print(f"Found {len(torrents)} torrents.")

        if torrents:
            print("\nTorrent list:")
            for i, torrent_data in enumerate(torrents[:5], 1):  # Show max 5 torrents
                print(
                    f"{i}. {torrent_data['name']} - {torrent_data['progress'] * 100:.1f}%"
                )

            if len(torrents) > 5:
                print(f"...and {len(torrents) - 5} more.")

        # Logout
        client.logout()
        print("Logged out successfully.")

    except QBittorrentAPIError as e:
        print(f"Error: {e}")
        print(
            "Your saved credentials may be invalid. Try clearing them and saving again."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
