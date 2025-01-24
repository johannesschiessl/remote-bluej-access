#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import socket
from pathlib import Path
import argparse
import platform
import webbrowser
import shutil
import websockify.websocketproxy
import requests

def is_windows():
    return platform.system() == "Windows"

def setup_ngrok(port):
    """Setup and start ngrok tunnel"""
    try:
        try:
            requests.get("http://localhost:4040/api/tunnels")
            print("Ngrok is already running")
            return
        except:
            pass

        subprocess.Popen([
            'ngrok', 'tcp', str(port),
            '--log', 'stdout'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()['tunnels']
            if tunnels:
                public_url = tunnels[0]['public_url']
                print(f"\nNgrok tunnel established: {public_url}")
                return public_url
        except Exception as e:
            print(f"Could not get ngrok URL: {e}")
            print("Please install ngrok from https://ngrok.com/download")
            print("And run: ngrok authtoken YOUR_AUTH_TOKEN")
    except FileNotFoundError:
        print("Ngrok not found. Please install ngrok from https://ngrok.com/download")
        print("And run: ngrok authtoken YOUR_AUTH_TOKEN")
    return None

def configure_tightvnc():
    """Configure TightVNC settings"""
    if is_windows():
        print("\nPlease configure TightVNC with these settings:")
        print("1. Right-click TightVNC icon in system tray")
        print("2. Click 'Configuration'")
        print("3. In 'Server' tab:")
        print("   - Check 'Accept incoming connections'")
        print("   - Set 'Main server port' to 5900")
        print("   - Uncheck 'Require VNC authentication'")
        print("4. Click OK")
        
        input("\nPress Enter after configuring TightVNC...")

def check_dependencies():
    """Check if required software is installed"""
    if is_windows():
        bluej_paths = [
            r"C:\Program Files\BlueJ",
            r"C:\Program Files (x86)\BlueJ",
        ]
        
        if not any(Path(p).exists() for p in bluej_paths):
            print("BlueJ not found! Please install BlueJ from: https://www.bluej.org")
            print("After installing BlueJ, run this script again.")
            sys.exit(1)
            
        if not Path(r"C:\Program Files\TightVNC").exists():
            print("TightVNC not found! Please install TightVNC from: https://www.tightvnc.com/download.php")
            print("After installing TightVNC, run this script again.")
            sys.exit(1)
            
        configure_tightvnc()

def setup_novnc():
    """Setup noVNC if not already present"""
    if not Path('noVNC').exists():
        print("Setting up noVNC...")
        try:
            subprocess.run(['git', 'clone', 'https://github.com/novnc/noVNC.git'], check=True)
            
            # Create a symbolic link for the VNC client
            if Path('noVNC/vnc.html').exists():
                os.chdir('noVNC')
                if is_windows():
                    if not Path('index.html').exists():
                        shutil.copy('vnc.html', 'index.html')
                else:
                    if not Path('index.html').exists():
                        os.symlink('vnc.html', 'index.html')
                os.chdir('..')
        except subprocess.CalledProcessError as e:
            print(f"Error setting up noVNC: {e}")
            sys.exit(1)

def start_vnc_server(geometry="1280x800"):
    """Start VNC server with specified geometry"""
    if is_windows():
        vnc_path = r"C:\Program Files\TightVNC\tvnserver.exe"
        if not Path(vnc_path).exists():
            print("Error: TightVNC not found!")
            sys.exit(1)
        
        subprocess.run(['net', 'start', 'tvnserver'], check=False)
        print("TightVNC service is running")
    else:
        subprocess.Popen(['vncserver', ':1', 
                         '-geometry', geometry, 
                         '-depth', '24',
                         '-localhost', 'no'])
        time.sleep(2)

class NoVNCProxy(websockify.websocketproxy.WebSocketProxy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def start_novnc(port=6080):
    """Start noVNC proxy using websockify"""
    try:
        print(f"Starting noVNC on port {port}...")
        
        server = NoVNCProxy(
            target_host="127.0.0.1",
            target_port=5900,
            listen_host="",
            listen_port=port,
            web=str(Path('noVNC').absolute()),
            heartbeat=30,
            verbose=True
        )
        
        return server
        
    except Exception as e:
        print(f"Error starting noVNC: {e}")
        sys.exit(1)

def get_ip_address():
    """Get the server's IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    parser = argparse.ArgumentParser(description='Start remote BlueJ access server')
    parser.add_argument('--port', type=int, default=6080, help='Port for noVNC (default: 6080)')
    parser.add_argument('--geometry', default='1280x800', help='Screen geometry (default: 1280x800)')
    parser.add_argument('--ngrok', action='store_true', help='Use ngrok for public access')
    args = parser.parse_args()

    print("🚀 Starting Remote BlueJ Access Server...")
    
    check_dependencies()
    setup_novnc()
    
    start_vnc_server(args.geometry)
    server = start_novnc(args.port)
    
    ngrok_url = None
    if args.ngrok:
        ngrok_url = setup_ngrok(args.port)
    
    ip_address = get_ip_address()
    local_url = f"http://{ip_address}:{args.port}/vnc.html"
    
    print("\n✨ Setup Complete! ✨")
    print(f"\nLocal access URL: {local_url}")
    if ngrok_url:
        print(f"Public access URL: {ngrok_url}")
    
    print("\nMake sure in TightVNC:")
    print("1. 'Accept incoming connections' is checked")
    print("2. 'Main server port' is set to 5900")
    print("3. Authentication is disabled or you know the password")
    
    time.sleep(2)
    webbrowser.open(local_url)
    
    print("\nPress Ctrl+C to stop the server")
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        server.stop()
        print("Server stopped")

if __name__ == "__main__":
    main() 