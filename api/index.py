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

class VercelPathMiddleware:
    """
    Normalizes PATH_INFO when Vercel rewrites requests to /api/index.py.
    Extracts the original request path from REQUEST_URI / RAW_URI or strips the /api/index.py prefix.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        raw_uri = environ.get('REQUEST_URI') or environ.get('RAW_URI') or environ.get('HTTP_X_FORWARDED_URI')
        if raw_uri:
            clean_path = raw_uri.split('?')[0]
            if clean_path and clean_path != '/api/index.py':
                environ['PATH_INFO'] = clean_path
        else:
            matched = environ.get('HTTP_X_MATCHED_PATH')
            if matched and matched != '/api/index.py':
                environ['PATH_INFO'] = matched
            else:
                path = environ.get('PATH_INFO', '')
                if path in ('/api/index.py', '/api/index', '/api'):
                    environ['PATH_INFO'] = '/'
                elif path.startswith('/api/index.py/'):
                    environ['PATH_INFO'] = path[len('/api/index.py'):]
                elif path.startswith('/api/index/'):
                    environ['PATH_INFO'] = path[len('/api/index'):]
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# WSGI compatibility for Vercel Python runtime
handler = app

if __name__ == "__main__":
    app.run()
