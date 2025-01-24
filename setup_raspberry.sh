#!/bin/bash

# Update system
echo "Updating system..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y \
    bluej \
    tigervnc-standalone-server \
    tigervnc-common \
    python3-pip \
    git \
    nginx \
    python3-venv \
    xfce4 \
    xfce4-goodies

# Create Python virtual environment
echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install websockify requests pathlib argparse

# Setup VNC password
echo "Setting up VNC..."
mkdir -p ~/.vnc
echo "Please set a VNC password:"
vncpasswd

# Create VNC startup script
echo "Creating VNC startup script..."
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
startxfce4 &
EOF

# Make startup script executable
chmod +x ~/.vnc/xstartup

# Create systemd service for VNC
echo "Creating VNC service..."
sudo tee /etc/systemd/system/vncserver.service << 'EOF'
[Unit]
Description=VNC Server
After=syslog.target network.target

[Service]
Type=forking
User=$USER
ExecStart=/usr/bin/vncserver :1 -geometry 1280x800 -depth 24
ExecStop=/usr/bin/vncserver -kill :1

[Install]
WantedBy=multi-user.target
EOF

# Enable and start VNC service
sudo systemctl daemon-reload
sudo systemctl enable vncserver
sudo systemctl start vncserver

# Clone the remote-bluej-access repository
echo "Setting up remote BlueJ access..."
git clone https://github.com/novnc/noVNC.git

echo "Setup complete!"
echo "To start the server, run:"
echo "python3 remote_bluej.py"
echo ""
echo "For public access, install ngrok and run:"
echo "python3 remote_bluej.py --ngrok" 