# qBittorrent Client

Python client library for interacting with the qBittorrent Web API (v5.0+).

## Structure

- `qbittorrent_client.py`: Main client implementation
- `torrent.py`: Torrent class for representing torrents
- `cli.py`: Command-line interface
- `example.py`: Example usage of the client
- `__init__.py`: Package initialization

## Quick Start

```python
from qbittorrent_client import QBittorrentClient, Torrent

# Create a client
client = QBittorrentClient("http://localhost:8080")

# Login
client.login("username", "password")

# Get torrents
torrents_data = client.get_torrents()
torrents = [Torrent(data) for data in torrents_data]

# Display torrent information
for torrent in torrents:
    print(f"{torrent.name} - {torrent.progress_percent:.1f}%")

# Logout
client.logout()
```

For more details, see the main README.md file in the parent directory.
