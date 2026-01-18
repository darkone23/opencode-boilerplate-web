import os
from pathlib import Path
from flask import Flask, send_from_directory
from boilerplate_app.web.routes import api

def create_app():
    static_dir = Path(__file__).parent.parent.parent.parent / 'frontend' / 'dist'
    
    app = Flask(__name__,
                template_folder='templates',
                static_folder=None)
    
    app.register_blueprint(api, url_prefix='/api')
    
    # Serve static files from Vite build output
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory(static_dir / 'assets', filename)
    
    @app.route('/vite.svg')
    def serve_vite_svg():
        return send_from_directory(static_dir, 'vite.svg')
    
    @app.route('/')
    def index():
        return send_from_directory(static_dir, 'index.html')
    
    return app
