from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

# Mock user database - in a real application, this would be stored securely
USERS = {
    "admin": {
        "password": "password",
        "role": "admin"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}

def register_auth_routes(app):
    @app.route('/auth/login', methods=['POST'])
    def login():
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
        
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        
        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400
        
        # Check if user exists and password is correct
        if username not in USERS or USERS[username]["password"] != password:
            return jsonify({"error": "Invalid username or password"}), 401
        
        # Create access token with a 1-day expiry
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity=username,  
            expires_delta=expires
        )
        
        return jsonify({"token": access_token}), 200
    
    @app.route('/auth/verify', methods=['GET'])
    @jwt_required()
    def verify_token():
        current_user = get_jwt_identity()
        return jsonify({"user": current_user, "authenticated": True}), 200
