from flask import request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import register_auth_routes
from .query_processor import QueryProcessor

# Initialize the query processor
query_processor = QueryProcessor()

def register_routes(app):
    # Register authentication routes
    register_auth_routes(app)
    
    @app.route('/query', methods=['POST'])
    @jwt_required()
    def process_query():
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
        
        query_text = request.json.get('query', '')
        if not query_text:
            return jsonify({"error": "Missing query parameter"}), 400
        
        # Process the query
        query_data = query_processor.process_query(query_text)
        
        # Execute the query
        result = query_processor.execute_query(query_data)
        
        # Combine the query data and results
        response = {
            "query": query_text,
            "parsed_query": query_data,
            "results": result
        }
        
        return jsonify(response), 200
    
    @app.route('/explain', methods=['POST'])
    @jwt_required()
    def explain_query():
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
        
        # Check if we're getting a query text or a parsed query
        if 'query' in request.json:
            query_text = request.json.get('query', '')
            if not query_text:
                return jsonify({"error": "Missing query parameter"}), 400
            
            # Process the query
            query_data = query_processor.process_query(query_text)
        elif 'parsed_query' in request.json:
            query_data = request.json.get('parsed_query', {})
            if not query_data:
                return jsonify({"error": "Invalid parsed_query parameter"}), 400
        else:
            return jsonify({"error": "Missing query or parsed_query parameter"}), 400
        
        # Explain the query
        explanation = query_processor.explain_query(query_data)
        
        response = {
            "explanation": explanation
        }
        
        return jsonify(response), 200
    
    @app.route('/validate', methods=['POST'])
    @jwt_required()
    def validate_query():
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
        
        # Check if we're getting a query text or a parsed query
        if 'query' in request.json:
            query_text = request.json.get('query', '')
            if not query_text:
                return jsonify({"error": "Missing query parameter"}), 400
            
            # Process the query
            query_data = query_processor.process_query(query_text)
        elif 'parsed_query' in request.json:
            query_data = request.json.get('parsed_query', {})
            if not query_data:
                return jsonify({"error": "Invalid parsed_query parameter"}), 400
        else:
            return jsonify({"error": "Missing query or parsed_query parameter"}), 400
        
        # Validate the query
        validation = query_processor.validate_query(query_data)
        
        response = {
            "validation": validation
        }
        
        return jsonify(response), 200
    
    # Add a simple health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200
        
    # Add a welcome page for the root URL
    @app.route('/', methods=['GET'])
    def welcome():
        return render_template('index.html')

    # Add a welcome page for the root URL
    @app.route('/api', methods=['GET'])
    def api_welcome():
        return jsonify({
            "message": "Welcome to the Mini Data Query Simulation Engine API",
            "endpoints": {
                "/auth/login": "Get authentication token (POST)",
                "/query": "Process natural language queries (POST)",
                "/explain": "Get explanation of a query (POST)",
                "/validate": "Validate a query (POST)",
                "/health": "Check API health (GET)"
            },
            "version": "1.0.0"
        }), 200
