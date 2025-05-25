# Password Caching in qBittorrent Client

## How It Works

This feature allows you to cache your qBittorrent WebUI credentials securely on your local machine, eliminating the need to enter your credentials each time you use the client.

### Security Considerations

- Passwords are base64-encoded (not encrypted) to avoid plain text storage
- The credentials file is stored in your system's temporary directory with restricted permissions (readable only by you)
- No sensitive information is transmitted over the network - all credentials are stored locally

## Usage

### Command-line Interface

```bash
# Cache credentials for future use
qbt --url http://localhost:8080 --username admin --cache-credentials

# Use cached credentials (no need to provide username/password)
qbt

# Clear cached credentials
qbt --clear-cached-credentials
```

### Programmatic Usage

```python
from qbittorrent_client import QBittorrentClient, CredentialsManager

# Initialize the credentials manager
credentials_manager = CredentialsManager()

# Save credentials
credentials_manager.save_credentials("http://localhost:8080", "username", "password")

# Get cached credentials
url, username, password = credentials_manager.get_url_username_password()

# Create a client using cached credentials
client = QBittorrentClient(url)
client.login(username, password)

# Clear cached credentials when needed
credentials_manager.clear_credentials()
```

## Where Credentials are Stored

Credentials are stored in a file named `.qbittorrent_credentials` in your system's temporary directory:

- Windows: `C:\Users\<Username>\AppData\Local\Temp`
- macOS: `/var/folders/...`
- Linux: `/tmp`

The file is created with permissions that restrict access to only your user account.
