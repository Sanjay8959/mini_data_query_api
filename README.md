# Mini Data Query Simulation Engine

A Flask-based REST API that simulates a natural language to SQL query engine with mock data.

## Features

- Natural language to SQL query conversion
- Query explanation and validation
- In-memory SQLite database with mock data
- JWT-based authentication
- Mock data for customers, products, and sales tables

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository or download the source code

2. Navigate to the project directory
   ```
   cd mini_data_query_api
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

The server will start on `http://localhost:5000` by default.

## API Documentation

### Authentication

All API endpoints (except `/health` and `/`) require JWT authentication.

#### Get Authentication Token

```
POST /auth/login
```

**Request Body:**
```json
{
  "username": "admin",
  "password": "password"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Available Users:**
- Username: `admin`, Password: `password`
- Username: `user`, Password: `user123`

### Query Operations

#### Process Natural Language Query

```
POST /query
```

Converts a natural language query to SQL and executes it against the database.

**Request Headers:**
- Authorization: Bearer {token}

**Request Body:**
```json
{
  "query": "Show me all sales from last month"
}
```

**Response:**
```json
{
  "query": "Show me all sales from last month",
  "parsed_query": {
    "entity": "sales",
    "operation": "select",
    "conditions": ["sale_date BETWEEN '2023-07-01' AND '2023-07-31'"],
    "sql": "SELECT * FROM sales WHERE sale_date BETWEEN '2023-07-01' AND '2023-07-31' LIMIT 10"
  },
  "results": {
    "success": true,
    "data": [...]
  }
}
```

#### Explain Query

```
POST /explain
```

Provides an explanation of a natural language query or a parsed query.

**Request Headers:**
- Authorization: Bearer {token}

**Request Body (Option 1 - Natural Language):**
```json
{
  "query": "Show me all sales from last month"
}
```

**Request Body (Option 2 - Parsed Query):**
```json
{
  "parsed_query": {
    "entity": "sales",
    "operation": "select",
    "conditions": ["sale_date BETWEEN '2023-07-01' AND '2023-07-31'"],
    "sql": "SELECT * FROM sales WHERE sale_date BETWEEN '2023-07-01' AND '2023-07-31' LIMIT 10"
  }
}
```

**Response:**
```json
{
  "explanation": {
    "summary": "This query is looking for select data from the sales table.",
    "details": [
      "The query will return all columns from the table.",
      "The query includes the following conditions:",
      "- sale_date BETWEEN '2023-07-01' AND '2023-07-31'"
    ],
    "sql": "SELECT * FROM sales WHERE sale_date BETWEEN '2023-07-01' AND '2023-07-31' LIMIT 10"
  }
}
```

#### Validate Query

```
POST /validate
```

Checks if a query is valid and can be executed against the database.

**Request Headers:**
- Authorization: Bearer {token}

**Request Body (Option 1 - Natural Language):**
```json
{
  "query": "Show me all sales from last month"
}
```

**Request Body (Option 2 - Parsed Query):**
```json
{
  "parsed_query": {
    "entity": "sales",
    "operation": "select",
    "conditions": ["sale_date BETWEEN '2023-07-01' AND '2023-07-31'"],
    "sql": "SELECT * FROM sales WHERE sale_date BETWEEN '2023-07-01' AND '2023-07-31' LIMIT 10"
  }
}
```

**Response:**
```json
{
  "validation": {
    "valid": true,
    "message": "The query is valid and can be executed successfully."
  }
}
```

### Other Endpoints

#### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

#### API Welcome Page

```
GET /api
```

**Response:**
```json
{
  "message": "Welcome to the Mini Data Query Simulation Engine API",
  "endpoints": {
    "/auth/login": "Get authentication token (POST)",
    "/query": "Process natural language queries (POST)",
    "/explain": "Get explanation of a query (POST)",
    "/validate": "Validate a query (POST)",
    "/health": "Check API health (GET)"
  },
  "version": "1.0.0"
}
```

## Sample Query Examples

The API supports various types of natural language queries:

1. **Basic Queries**
   - "Show me all customers"
   - "List all products"
   - "Get all sales"

2. **Aggregation Queries**
   - "Count all customers"
   - "What is the total sales amount?"
   - "What is the average product price?"
   - "What is the most expensive product?"
   - "What is the cheapest product in Electronics?"

3. **Filtered Queries**
   - "Show me all sales from last month"
   - "Find all products in the Electronics category"
   - "Show me all products under $100"
   - "List all sales from this year"

## Testing with Postman

### Postman Collection

You can import the following Postman collection to test the API:

1. Create a new collection in Postman
2. Add the following requests:

#### Login Request
- Method: POST
- URL: http://localhost:5000/auth/login
- Body (raw, JSON):
```json
{
  "username": "admin",
  "password": "password"
}
```

#### Query Request
- Method: POST
- URL: http://localhost:5000/query
- Auth: Bearer Token (use the token from the login response)
- Body (raw, JSON):
```json
{
  "query": "Show me all sales from last month"
}
```

#### Explain Request
- Method: POST
- URL: http://localhost:5000/explain
- Auth: Bearer Token (use the token from the login response)
- Body (raw, JSON):
```json
{
  "query": "Show me all sales from last month"
}
```

#### Validate Request
- Method: POST
- URL: http://localhost:5000/validate
- Auth: Bearer Token (use the token from the login response)
- Body (raw, JSON):
```json
{
  "query": "Show me all sales from last month"
}
```

## Testing with cURL

### Authentication
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"password"}' http://localhost:5000/auth/login
```

### Query
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN_HERE" -d '{"query":"Show me all sales from last month"}' http://localhost:5000/query
```

### Explain
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN_HERE" -d '{"query":"Show me all sales from last month"}' http://localhost:5000/explain
```

### Validate
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN_HERE" -d '{"query":"Show me all sales from last month"}' http://localhost:5000/validate
```

## Database Schema

The API uses an in-memory SQLite database with the following tables:

### Customers
- id (INTEGER, PRIMARY KEY)
- name (TEXT)
- email (TEXT)
- signup_date (TEXT)

### Products
- id (INTEGER, PRIMARY KEY)
- name (TEXT)
- category (TEXT)
- price (REAL)
- inventory (INTEGER)

### Sales
- id (INTEGER, PRIMARY KEY)
- customer_id (INTEGER, FOREIGN KEY)
- product_id (INTEGER, FOREIGN KEY)
- quantity (INTEGER)
- sale_date (TEXT)
- total_price (REAL)

## Limitations

- The API uses an in-memory database, so all data is lost when the server is restarted
- The natural language processing is simulated and limited to specific patterns
- Authentication is basic and not suitable for production use
