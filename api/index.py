"""
Vercel Serverless Function entry point.
"""
from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

# For WSGI compatibility
handler = app

if __name__ == "__main__":
    app.run()

