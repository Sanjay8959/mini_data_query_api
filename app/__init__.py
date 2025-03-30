# Make create_app function available at the package level
# This allows "from app import create_app" to work
from app.routes import register_routes
from app.database import init_db
from flask import Flask
from flask_jwt_extended import JWTManager
import os

def create_app():
    # Create Flask app with explicit template folder path
    app = Flask(__name__, 
                template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')))
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize database
    init_db()
    
    # Register routes
    register_routes(app)
    
    return app
