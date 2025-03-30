import requests
import json
import sys

# Set default BASE_URL, but allow it to be overridden by command-line argument
BASE_URL = 'http://localhost:5000'
if len(sys.argv) > 1:
    BASE_URL = sys.argv[1]
    print(f"Using API endpoint: {BASE_URL}")

def test_api():
    """Test the Mini Data Query Simulation Engine API"""
    print("Testing Mini Data Query Simulation Engine API")
    
    # Step 1: Get authentication token
    print("\n1. Getting authentication token...")
    auth_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "password"}
    )
    
    if auth_response.status_code != 200:
        print(f"Authentication failed: {auth_response.text}")
        return
    
    token = auth_response.json().get('token')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    print("Authentication successful!")
    
    # Step 2: Test the query endpoint
    print("\n2. Testing /query endpoint...")
    query_tests = [
        "Show me all sales from last month",
        "Count all products in Electronics category",
        "What is the average price of products?",
        "Find the most expensive product in the store",
        "What is the cheapest item in Clothing category?"
    ]
    
    for query in query_tests:
        print(f"\nQuery: {query}")
        query_response = requests.post(
            f"{BASE_URL}/query",
            headers=headers,
            json={"query": query}
        )
        
        if query_response.status_code != 200:
            print(f"Query failed: {query_response.text}")
            continue
        
        result = query_response.json()
        print(f"SQL: {result['parsed_query']['sql']}")
        print(f"Results: {json.dumps(result['results'], indent=2)}")
        
        # Step 3: Test the explain endpoint with the same query
        print("\nTesting /explain endpoint...")
        explain_response = requests.post(
            f"{BASE_URL}/explain",
            headers=headers,
            json={"query": query}
        )
        
        if explain_response.status_code != 200:
            print(f"Explain failed: {explain_response.text}")
            continue
        
        explanation = explain_response.json()
        print(f"Explanation: {explanation['explanation']['summary']}")
        print(f"Details: {json.dumps(explanation['explanation']['details'], indent=2)}")
        
        # Step 4: Test the validate endpoint with the same query
        print("\nTesting /validate endpoint...")
        validate_response = requests.post(
            f"{BASE_URL}/validate",
            headers=headers,
            json={"query": query}
        )
        
        if validate_response.status_code != 200:
            print(f"Validate failed: {validate_response.text}")
            continue
        
        validation = validate_response.json()
        print(f"Validation: {json.dumps(validation['validation'], indent=2)}")
    
    # Step 5: Test health check endpoint
    print("\n5. Testing /health endpoint...")
    health_response = requests.get(f"{BASE_URL}/health")
    
    if health_response.status_code != 200:
        print(f"Health check failed: {health_response.text}")
        return
    
    print(f"Health check: {health_response.json()}")
    print("\nAPI testing completed!")

if __name__ == "__main__":
    test_api()
