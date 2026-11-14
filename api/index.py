"""
Vercel Serverless Function entry point.
"""
import sys
import os
from pathlib import Path

# Add project root directory to sys.path so 'app' package is discoverable by Python on Vercel
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
env_file = project_root / '.env'
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()

from app import create_app

app = create_app()

# WSGI compatibility for Vercel Python runtime
handler = app

if __name__ == "__main__":
    app.run()
