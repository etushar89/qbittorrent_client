#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QBittorrent CLI Module

This module provides a command-line interface for the QBittorrent client.
"""

import sys
import argparse
import getpass
import logging

from qbittorrent_client.qbittorrent_client import QBittorrentClient, QBittorrentAPIError
from qbittorrent_client.torrent import Torrent
from qbittorrent_client.credentials import CredentialsManager


def setup_logging() -> logging.Logger:
    """
    Set up logging for the CLI application.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger("qbittorrent_cli")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="QBittorrent Client CLI")

    parser.add_argument(
        "--url",
        default="http://localhost:8080",
        help="QBittorrent WebUI URL (default: http://localhost:8080)",
    )

    parser.add_argument("--username", help="QBittorrent WebUI username")

    parser.add_argument(
        "--password", help="QBittorrent WebUI password (will prompt if not provided)"
    )

    parser.add_argument(
        "--cache-credentials",
        action="store_true",
        help="Cache credentials for future use",
    )

    parser.add_argument(
        "--clear-cached-credentials",
        action="store_true",
        help="Clear cached credentials",
    )

    parser.add_argument(
        "--filter",
        default="all",
        choices=[
            "all",
            "downloading",
            "seeding",
            "completed",
            "paused",
            "active",
            "inactive",
        ],
        help="Filter torrents by status (default: all)",
    )

    parser.add_argument("--sort", help="Sort torrents by field")

    parser.add_argument("--reverse", action="store_true", help="Reverse sort order")

    parser.add_argument("--limit", type=int, help="Limit number of torrents to show")

    parser.add_argument("--category", help="Filter by category")

    parser.add_argument("--tag", help="Filter by tag")

    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed information for each torrent",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args()


def display_torrent(torrent: Torrent, detailed: bool = False) -> None:
    """
    Display information about a torrent.

    Args:
        torrent: The torrent to display information for.
        detailed: Whether to show detailed information.
    """
    # Basic display format
    status_emoji = (
        "⬇️ "
        if torrent.is_downloading
        else "⬆️ " if torrent.is_uploading else "⏸️ " if torrent.is_paused else "⏳ "
    )

    print(f"{status_emoji} {torrent.name} [{torrent.progress_percent:.1f}%]")

    if detailed:
        # Print additional information if detailed view is requested
        print(f"  Hash: {torrent.hash}")
        print(f"  Size: {torrent.size_formatted}")
        print(f"  State: {torrent.state}")
        print(f"  Download speed: {torrent.download_speed_formatted}")
        print(f"  Upload speed: {torrent.upload_speed_formatted}")
        print(f"  ETA: {torrent.eta_formatted}")
        print(f"  Seeds: {torrent.num_seeds}")
        print(f"  Peers: {torrent.num_leechs}")
        if torrent.category:
            print(f"  Category: {torrent.category}")
        if torrent.tags:
            print(f"  Tags: {torrent.tags}")
        print(f"  Added on: {torrent.added_on.strftime('%Y-%m-%d %H:%M:%S')}")
        if torrent.completion_on:
            print(
                f"  Completed on: {torrent.completion_on.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        print()


def main() -> None:
    """
    Main entry point for the CLI application.
    """
    args = parse_arguments()
    logger = setup_logging()

    # Set log level based on verbosity
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Initialize credentials manager
    credentials_manager = CredentialsManager()

    # Handle clear cached credentials request
    if args.clear_cached_credentials:
        if credentials_manager.clear_credentials():
            print("Cached credentials cleared successfully.")
        else:
            print("No cached credentials found.")
        return

    # Try to get credentials from cache or command line arguments
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

        # Save credentials if requested
        if args.cache_credentials:
            credentials_manager.save_credentials(url, username, password)
            print("Credentials cached successfully.")

        # Display version information
        api_version = client.get_api_version()
        app_version = client.get_app_version()
        print(f"Connected to qBittorrent {app_version} (API v{api_version})")

        # Prepare parameters for get_torrents
        params = {}
        if args.sort:
            params["sort"] = args.sort
        if args.reverse:
            params["reverse"] = "true"
        if args.limit:
            params["limit"] = args.limit
        if args.category:
            params["category"] = args.category
        if args.tag:
            params["tag"] = args.tag

        # Get torrents
        torrents_data = client.get_torrents(filter_status=args.filter, **params)

        # Convert raw data to Torrent objects
        torrents = [Torrent(data) for data in torrents_data]

        # Display torrent information
        if not torrents:
            print("No torrents found.")
        else:
            print(f"Found {len(torrents)} torrents:")
            print("-" * 60)
            for torrent in torrents:
                display_torrent(torrent, args.detailed)
                if not args.detailed:
                    print()

        # Logout
        client.logout()

    except QBittorrentAPIError as error:
        logger.error(f"Error: {error}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
