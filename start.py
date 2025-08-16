#!/usr/bin/env python3
"""
Wallet Platform Startup Script
This script helps you start the wallet platform easily.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print the platform banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    Wallet Connection Platform                 ║
║                                                              ║
║  A modern Web3 platform for wallet connections and          ║
║  transactions. Create links, connect wallets, and           ║
║  perform transactions seamlessly.                            ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        sys.exit(1)
    print("✅ Python version check passed")

def install_backend_dependencies():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("❌ Error: Backend directory not found")
        return False
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing backend dependencies: {e}")
        return False

def start_backend():
    """Start the Flask backend server"""
    print("\n🚀 Starting backend server...")
    
    try:
        # Get the current working directory
        current_dir = os.getcwd()
        backend_dir = os.path.join(current_dir, "backend")
        
        # Check if backend directory exists
        if not os.path.exists(backend_dir):
            print(f"❌ Backend directory not found at: {backend_dir}")
            return None
        
        # Start the server from the backend directory
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            cwd=backend_dir
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        print("✅ Backend server started at http://localhost:5000")
        print("📊 Admin dashboard: http://localhost:5000/admin")
        print("🌐 Main site: http://localhost:5000")
        
        return process
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def open_browsers():
    """Open the platform in browser"""
    print("\n🌍 Opening platform in browser...")
    
    try:
        # Open main site
        webbrowser.open("http://localhost:5000")
        time.sleep(1)
        
        # Open admin dashboard
        webbrowser.open("http://localhost:5000/admin")
        
        print("✅ Platform opened in browser")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")

def main():
    """Main startup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_backend_dependencies():
        print("❌ Failed to install dependencies. Exiting.")
        sys.exit(1)
    
    # Start backend (now serves both backend API and frontend pages)
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        sys.exit(1)
    
    # Open browsers
    open_browsers()
    
    print("\n🎉 Wallet Platform is now running!")
    print("\n📋 Quick Guide:")
    print("1. Go to http://localhost:5000/admin to create connection links")
    print("2. Share the generated links with users")
    print("3. Users can connect their wallets through the links")
    print("4. Monitor connections and transactions in the admin dashboard")
    print("\n🛑 Press Ctrl+C to stop the server")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        
        # Terminate process
        if backend_process:
            backend_process.terminate()
        
        print("✅ Server stopped")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main() 