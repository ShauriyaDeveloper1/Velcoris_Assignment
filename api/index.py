"""
Vercel Serverless Function entry point.
"""
import sys
import os
from pathlib import Path
from urllib.parse import parse_qs, urlencode

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
    Normalizes PATH_INFO when Vercel rewrites requests to /api/index.py?path=$1.
    Extracts the original request path from 'path' query parameter or headers.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = parse_qs(environ.get('QUERY_STRING', ''), keep_blank_values=True)
        if 'path' in qs:
            val = qs.pop('path')[0]
            environ['PATH_INFO'] = ('/' + val.lstrip('/')) if val else '/'
            environ['QUERY_STRING'] = urlencode(qs, doseq=True)
        elif environ.get('HTTP_X_MATCHED_PATH') and environ.get('HTTP_X_MATCHED_PATH') != '/api/index.py':
            environ['PATH_INFO'] = environ['HTTP_X_MATCHED_PATH']
        else:
            raw_uri = environ.get('REQUEST_URI') or environ.get('RAW_URI') or environ.get('HTTP_X_FORWARDED_URI')
            if raw_uri:
                clean_path = raw_uri.split('?')[0]
                if clean_path and clean_path != '/api/index.py':
                    environ['PATH_INFO'] = clean_path
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
