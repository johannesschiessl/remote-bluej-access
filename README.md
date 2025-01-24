# Remote BlueJ Access

Access BlueJ through a web browser from anywhere. Perfect for situations where people can't install BlueJ locally.

## Features

- Access BlueJ through any web browser
- Works on both Windows and Raspberry Pi
- Optional public access through ngrok
- Simple setup process
- Low-latency remote access

## Setup Instructions

### Windows Setup

1. **Install Required Software:**
   - Install [BlueJ](https://www.bluej.org)
   - Install [TightVNC Server](https://www.tightvnc.com/download.php)
   - Install [Python 3.x](https://www.python.org/downloads/)
   - Install [Git](https://git-scm.com/downloads)

2. **Clone and Setup:**
   ```bash
   # Clone the repository
   git clone https://github.com/johannesschiessl/remote-bluej-access.git
   cd remote-bluej-access

   # Create virtual environment
   python -m venv .venv
   .venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure TightVNC:**
   - Right-click TightVNC icon in system tray
   - Click 'Configuration'
   - In 'Server' tab:
     - Check 'Accept incoming connections'
     - Set 'Main server port' to 5900
     - Configure authentication as needed

### Raspberry Pi Setup

1. **Install Raspberry Pi OS:**
   - Download [Raspberry Pi OS with Desktop](https://www.raspberrypi.com/software/)
   - Install it to your SD card
   - Complete initial setup and connect to network

2. **Quick Setup:**
   ```bash
   # Clone the repository
   git clone https://github.com/johannesschiessl/remote-bluej-access.git
   cd remote-bluej-access

   # Make setup script executable
   chmod +x setup_raspberry.sh

   # Run setup script
   ./setup_raspberry.sh
   ```

The setup script will automatically:
- Install all required packages
- Configure VNC server
- Set up Python environment
- Create startup services

## Usage

### Starting the Server

**Windows:**
```bash
# Activate virtual environment
.venv\Scripts\activate

# Start server (local access only)
python remote_bluej.py

# Start server with public access
python remote_bluej.py --ngrok
```

**Raspberry Pi:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Start server (local access only)
python3 remote_bluej.py

# Start server with public access
python3 remote_bluej.py --ngrok
```

### Accessing BlueJ

1. **Local Access:**
   - Open browser and go to the URL shown in terminal
   - Usually: `http://YOUR_IP:6080/vnc.html`

2. **Public Access (with ngrok):**
   - Install ngrok from https://ngrok.com/download
   - Set up ngrok authentication token
   - Use the `--ngrok` flag when starting the server
   - Access through the ngrok URL provided

### Command Line Options

```bash
python remote_bluej.py [OPTIONS]

Options:
  --port PORT       Port for noVNC (default: 6080)
  --geometry WxH    Screen resolution (default: 1280x800)
  --ngrok          Enable public access through ngrok
```

## Requirements

### Windows:
- Windows 10 or later
- Python 3.7+
- BlueJ
- TightVNC Server

### Raspberry Pi:
- Raspberry Pi 3 or better (4 recommended)
- 2GB+ RAM recommended
- Raspberry Pi OS with Desktop
- Python 3.7+

## Troubleshooting

1. **Connection Refused:**
   - Check if TightVNC service is running
   - Verify port 5900 is not blocked by firewall
   - Make sure 'Accept incoming connections' is enabled

2. **Black Screen:**
   - Restart TightVNC service
   - Check VNC server logs
   - Verify desktop environment is running

3. **Performance Issues:**
   - Lower the screen resolution using --geometry
   - Use a wired network connection if possible
   - On Raspberry Pi, consider overclocking

## Security Notes

- By default, connections are unencrypted
- For public access, consider:
  - Enabling VNC authentication
  - Using HTTPS (via nginx)
  - Setting up a firewall
  - Regular system updates

## Contributing

Feel free to open issues or submit pull requests!

## License

[MIT License](LICENSE)
