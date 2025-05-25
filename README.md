# qBittorrent Client

[![Python Checks](https://github.com/etushar89/qbittorrent-client/actions/workflows/python-checks.yml/badge.svg)](https://github.com/etushar89/qbittorrent-client/actions/workflows/python-checks.yml)

A Python client for interacting with the qBittorrent Web API (v5.0+).

## Features

- Authentication with qBittorrent's Web API
- Retrieve list of torrents with comprehensive information
- Object-oriented design with Torrent objects
- Command-line interface for quick access
- API for programmatic usage
- [Secure credential caching](docs/password-caching.md) for improved user experience

## Installation

### From Source

```bash
git clone https://github.com/etushar89/qbittorrent-client.git
cd qbittorrent-client
pip install -e .
```

## Usage

### Command-line Interface

The package includes a command-line interface for interacting with qBittorrent:

```bash
# Show all torrents
qbt --url http://localhost:8080 --username admin

# Show only downloading torrents
qbt --filter downloading

# Show detailed information
qbt --detailed

# Sort by size in descending order
qbt --sort size --reverse

# Filter by category
qbt --category "movies"

# Cache credentials for future use
qbt --url http://localhost:8080 --username admin --cache-credentials

# Use cached credentials (no need to provide username/password again)
qbt

# Clear cached credentials
qbt --clear-cached-credentials
```

### Programmatic Usage

```python
from qbittorrent_client import QBittorrentClient, Torrent

# Create a client
client = QBittorrentClient("http://localhost:8080")

# Login
client.login("username", "password")

# Get torrents
torrents_data = client.get_torrents(filter_status="downloading")
torrents = [Torrent(data) for data in torrents_data]

# Display torrent information
for torrent in torrents:
    print(f"{torrent.name} - {torrent.progress_percent:.1f}%")
    print(f"Download speed: {torrent.download_speed_formatted}")
    print(f"ETA: {torrent.eta_formatted}")

# Get properties of a specific torrent
torrent_hash = torrents[0].hash
properties = client.get_torrent_properties(torrent_hash)

# Logout
client.logout()
```

## API Documentation

### QBittorrentClient

The main class for interacting with the qBittorrent Web API.

#### Methods

- `login(username, password)`: Authenticate with the qBittorrent WebUI
- `logout()`: Log out from the WebUI
- `get_torrents(filter_status='all', **kwargs)`: Get a list of torrents
- `get_torrent_properties(torrent_hash)`: Get properties of a specific torrent
- `get_app_version()`: Get the qBittorrent application version
- `get_api_version()`: Get the qBittorrent Web API version

### Torrent

A class representing a torrent in qBittorrent.

#### Properties

- `hash`: The torrent hash
- `name`: The torrent name
- `size`: The torrent size in bytes
- `progress`: The torrent progress (0-1)
- `dlspeed`: Download speed in bytes per second
- `upspeed`: Upload speed in bytes per second
- `num_seeds`: Number of seeds
- `num_leechs`: Number of peers
- `state`: Current state of the torrent
- And many more...

#### Convenience Properties

- `progress_percent`: The progress as a percentage (0-100)
- `is_complete`: Whether the torrent is complete
- `is_downloading`: Whether the torrent is downloading
- `is_uploading`: Whether the torrent is uploading/seeding
- `is_paused`: Whether the torrent is paused
- `download_speed_formatted`: Human-readable download speed
- `upload_speed_formatted`: Human-readable upload speed
- `size_formatted`: Human-readable size
- `eta_formatted`: Human-readable ETA

## Requirements

- Python 3.7+
- requests library

## Development

### Setting Up Development Environment

```bash
# Install package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=qbittorrent_client

# Run specific test file
pytest qbittorrent_client/tests/test_torrent.py
```

### Code Formatting and Linting

```bash
# Format code with Black
black qbittorrent_client

# Sort imports
isort qbittorrent_client

# Run flake8 linting
flake8 qbittorrent_client

# Run type checking
mypy qbittorrent_client
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
