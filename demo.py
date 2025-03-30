import requests
import json

BASE_URL = 'http://localhost:5000'

def demo_api():
    """Demonstrate the Mini Data Query Simulation Engine API with clear examples"""
    print("=== Mini Data Query Simulation Engine API Demo ===")
    
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
    print("✓ Authentication successful!")
    
    # Step 2: Demonstrate each endpoint with specific examples
    demo_queries = [
        {
            "name": "Find most expensive product",
            "query": "What is the most expensive product in the store?",
            "description": "This query finds the product with the highest price"
        },
        {
            "name": "Find cheapest clothing item",
            "query": "What is the cheapest item in the Clothing category?",
            "description": "This query finds the cheapest product in a specific category"
        },
        {
            "name": "Count electronics products",
            "query": "How many products are in the Electronics category?",
            "description": "This query counts products in a specific category"
        },
        {
            "name": "Average product price",
            "query": "What is the average price of all products?",
            "description": "This query calculates the average price across all products"
        }
    ]
    
    for demo in demo_queries:
        print(f"\n\n=== DEMO: {demo['name']} ===")
        print(f"Description: {demo['description']}")
        print(f"Natural language query: \"{demo['query']}\"")
        
        # 1. Process the query
        print("\n1. Sending to /query endpoint...")
        query_response = requests.post(
            f"{BASE_URL}/query",
            headers=headers,
            json={"query": demo['query']}
        )
        
        if query_response.status_code != 200:
            print(f"Query failed: {query_response.text}")
            continue
        
        result = query_response.json()
        print(f"Generated SQL: {result['parsed_query']['sql']}")
        print("\nResults:")
        print(json.dumps(result['results']['data'], indent=2))
        
        # 2. Explain the query
        print("\n2. Sending to /explain endpoint...")
        explain_response = requests.post(
            f"{BASE_URL}/explain",
            headers=headers,
            json={"query": demo['query']}
        )
        
        if explain_response.status_code != 200:
            print(f"Explain failed: {explain_response.text}")
            continue
        
        explanation = explain_response.json()
        print(f"Explanation: {explanation['explanation']['summary']}")
        print("Details:")
        for detail in explanation['explanation']['details']:
            print(f"- {detail}")
        
        # 3. Validate the query
        print("\n3. Sending to /validate endpoint...")
        validate_response = requests.post(
            f"{BASE_URL}/validate",
            headers=headers,
            json={"query": demo['query']}
        )
        
        if validate_response.status_code != 200:
            print(f"Validate failed: {validate_response.text}")
            continue
        
        validation = validate_response.json()
        print(f"Validation result: {'✓ Valid' if validation['validation']['valid'] else '✗ Invalid'}")
        if 'message' in validation['validation']:
            print(f"Message: {validation['validation']['message']}")
    
    print("\n\n=== Demo completed successfully! ===")

if __name__ == "__main__":
    demo_api()
