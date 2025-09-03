#!/usr/bin/env python3
"""
Script to run the application with HTTPS enabled.
This script sets the USE_HTTPS environment variable and runs the app.
"""
import os
import sys
import subprocess

def main():
    # Set environment variable to enable HTTPS
    os.environ["USE_HTTPS"] = "True"
    
    print("🔒 Starting application with HTTPS enabled...")
    print("📁 SSL certificates should be in: certs/cert.pem and certs/key.pem")
    print("🌐 Application will be available at: https://localhost:8000")
    print("📚 API docs will be available at: https://localhost:8000/docs")
    print("⚠️  Note: You'll see a security warning due to self-signed certificate")
    print("-" * 60)
    
    try:
        # Run the application
        subprocess.run([sys.executable, "-m", "app.main"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())