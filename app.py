from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes import register_routes
from app.database import init_db
import os

def create_app():
    app = Flask(__name__)
    
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

# Create the application instance - this is what Gunicorn will look for
application = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)
