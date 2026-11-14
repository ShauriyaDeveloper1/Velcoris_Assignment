from flask import Flask
from pathlib import Path
import os
from dotenv import load_dotenv
from .db import init_db

# Load environment variables from .env file in the project root
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Detect serverless or read-only container environments (Vercel, AWS Lambda, etc.)
    is_serverless = any([
        os.environ.get('VERCEL'),
        os.environ.get('VERCEL_ENV'),
        os.environ.get('AWS_LAMBDA_FUNCTION_NAME'),
        os.environ.get('LAMBDA_TASK_ROOT'),
        os.environ.get('NOW_REGION')
    ])

    raw_db_path = os.environ.get('DATABASE_PATH')
    if is_serverless:
        # On serverless, always ensure database is stored in writable /tmp
        db_path = Path(raw_db_path or '/tmp/velcoris.db')
        if not db_path.is_absolute():
            db_path = Path('/tmp') / db_path.name
    elif raw_db_path:
        db_path = Path(raw_db_path)
        if not db_path.is_absolute():
            db_path = (project_root / db_path).resolve()
    else:
        db_path = (Path(app.instance_path) / 'velcoris.db').resolve()

    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Fallback to /tmp if parent directory cannot be written
        db_path = Path('/tmp/velcoris.db')
        try:
            db_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    try:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'local-development-only-change-this'),
        DATABASE=str(db_path),
        ADMIN_USERNAME=os.environ.get('ADMIN_USERNAME', 'admin'),
        ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD', 'ChangeThisPassword123!'),
        MAX_CONTENT_LENGTH=16 * 1024,
    )
    init_db(app)
    from .routes import bp
    app.register_blueprint(bp)

    @app.cli.command('view-enquiries')
    def view_enquiries_command():
        """CLI command to inspect stored queries directly from terminal."""
        import sqlite3
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM enquiries ORDER BY id DESC').fetchall()
        print(f"\nTotal Enquiries in Database ({app.config['DATABASE']}): {len(rows)}\n" + "-"*80)
        for r in rows:
            print(f"[{r['id']}] {r['created_at']} | Status: {r['status']} | Type: {r['enquiry_type']}")
            print(f"    From: {r['name']} <{r['email']}> | Org: {r['organisation'] or 'N/A'}")
            print(f"    Subject: {r['subject']}")
            print(f"    Message: {r['message']}\n" + "-"*80)
        conn.close()

    @app.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data: https:; form-action 'self'; frame-ancestors 'none'"
        return response
    return app
