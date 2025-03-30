import re
import json
from datetime import datetime, timedelta
from .database import execute_query

class QueryProcessor:
    """
    Processes natural language queries and converts them to SQL-like statements
    """
    
    def __init__(self):
        # Keywords to identify query intent
        self.keywords = {
            'select': ['show', 'get', 'find', 'list', 'display', 'retrieve'],
            'count': ['count', 'how many', 'total number'],
            'sum': ['sum', 'total', 'add up'],
            'average': ['average', 'avg', 'mean'],
            'max': ['maximum', 'highest', 'most expensive', 'largest'],
            'min': ['minimum', 'lowest', 'cheapest', 'smallest']
        }
        
        # Entity mapping
        self.entities = {
            'customers': ['customers', 'users', 'clients', 'buyers'],
            'products': ['products', 'items', 'goods', 'merchandise'],
            'sales': ['sales', 'purchases', 'transactions', 'orders']
        }
        
        # Time period mapping
        self.time_periods = {
            'last month': self._get_last_month_range(),
            'this month': self._get_this_month_range(),
            'last year': self._get_last_year_range(),
            'this year': self._get_this_year_range()
        }
    
    def _get_last_month_range(self):
        today = datetime.now()
        first_day_of_month = datetime(today.year, today.month, 1)
        last_month = first_day_of_month - timedelta(days=1)
        first_day_of_last_month = datetime(last_month.year, last_month.month, 1)
        return {
            'start': first_day_of_last_month.strftime('%Y-%m-%d'),
            'end': last_month.strftime('%Y-%m-%d')
        }
    
    def _get_this_month_range(self):
        today = datetime.now()
        first_day_of_month = datetime(today.year, today.month, 1)
        return {
            'start': first_day_of_month.strftime('%Y-%m-%d'),
            'end': today.strftime('%Y-%m-%d')
        }
    
    def _get_last_year_range(self):
        today = datetime.now()
        first_day_of_year = datetime(today.year, 1, 1)
        last_year = datetime(today.year - 1, 1, 1)
        last_day_of_last_year = datetime(today.year - 1, 12, 31)
        return {
            'start': last_year.strftime('%Y-%m-%d'),
            'end': last_day_of_last_year.strftime('%Y-%m-%d')
        }
    
    def _get_this_year_range(self):
        today = datetime.now()
        first_day_of_year = datetime(today.year, 1, 1)
        return {
            'start': first_day_of_year.strftime('%Y-%m-%d'),
            'end': today.strftime('%Y-%m-%d')
        }
    
    def _identify_operation(self, query):
        """Identify the main operation in the query"""
        for operation, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword.lower() in query.lower():
                    return operation
        return 'select'  # Default to select if no operation is found
    
    def _identify_entity(self, query):
        """Identify the main entity in the query"""
        # Special case handling for specific queries
        if any(term in query.lower() for term in ['expensive', 'cheapest', 'price', 'cost']):
            return 'products'  # Price-related queries should use products table
            
        for entity, synonyms in self.entities.items():
            for synonym in synonyms:
                if synonym.lower() in query.lower():
                    return entity
        return 'sales'  # Default to sales if no entity is found
    
    def _identify_time_period(self, query):
        """Identify time period in the query"""
        for period, range_data in self.time_periods.items():
            if period.lower() in query.lower():
                return period, range_data
        return None, None
    
    def _identify_conditions(self, query, entity):
        """Identify conditions in the query"""
        conditions = []
        
        # Check for category conditions (for products)
        if entity == 'products':
            categories = ['Electronics', 'Clothing', 'Footwear', 'Home Appliances']
            for category in categories:
                if category.lower() in query.lower():
                    conditions.append(f"category = '{category}'")
        
        # Check for price conditions
        price_pattern = r'(under|over|less than|more than|cheaper than|expensive than)\s+\$?(\d+)'
        price_matches = re.findall(price_pattern, query.lower())
        
        for match in price_matches:
            operator, amount = match
            if operator in ['under', 'less than', 'cheaper than']:
                conditions.append(f"price < {amount}")
            elif operator in ['over', 'more than', 'expensive than']:
                conditions.append(f"price > {amount}")
        
        # Check for time period conditions
        period_name, period_range = self._identify_time_period(query)
        if period_name and entity == 'sales':
            conditions.append(f"sale_date BETWEEN '{period_range['start']}' AND '{period_range['end']}'")
        
        return conditions
    
    def process_query(self, query_text):
        """Process a natural language query and convert it to a pseudo-SQL query"""
        entity = self._identify_entity(query_text)
        operation = self._identify_operation(query_text)
        conditions = self._identify_conditions(query_text, entity)
        
        # Special case handling for specific query patterns
        if "most expensive" in query_text.lower() or "highest price" in query_text.lower():
            entity = 'products'
            sql = "SELECT * FROM products"
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            sql += " ORDER BY price DESC LIMIT 1"
            return {
                "entity": entity,
                "operation": "max",
                "conditions": conditions,
                "sql": sql
            }
            
        if "cheapest" in query_text.lower() or "lowest price" in query_text.lower():
            entity = 'products'
            sql = "SELECT * FROM products"
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            sql += " ORDER BY price ASC LIMIT 1"
            return {
                "entity": entity,
                "operation": "min",
                "conditions": conditions,
                "sql": sql
            }
        
        # Build the SQL query for standard cases
        if operation == 'select':
            sql = f"SELECT * FROM {entity}"
        elif operation == 'count':
            sql = f"SELECT COUNT(*) FROM {entity}"
        elif operation == 'sum':
            if entity == 'sales':
                sql = "SELECT SUM(total_price) FROM sales"
            elif entity == 'products':
                sql = "SELECT SUM(price * inventory) FROM products"
            else:
                sql = f"SELECT COUNT(*) FROM {entity}"
        elif operation == 'average':
            if entity == 'sales':
                sql = "SELECT AVG(total_price) FROM sales"
            elif entity == 'products':
                sql = "SELECT AVG(price) FROM products"
            else:
                sql = f"SELECT COUNT(*) FROM {entity}"
        elif operation == 'max':
            if entity == 'sales':
                sql = "SELECT MAX(total_price) FROM sales"
            elif entity == 'products':
                sql = "SELECT MAX(price) FROM products"
            else:
                sql = f"SELECT * FROM {entity} ORDER BY id DESC LIMIT 1"
        elif operation == 'min':
            if entity == 'sales':
                sql = "SELECT MIN(total_price) FROM sales"
            elif entity == 'products':
                sql = "SELECT MIN(price) FROM products"
            else:
                sql = f"SELECT * FROM {entity} ORDER BY id ASC LIMIT 1"
        
        # Add conditions if any
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        # Add limit for select queries
        if operation == 'select':
            sql += " LIMIT 10"
        
        return {
            "entity": entity,
            "operation": operation,
            "conditions": conditions,
            "sql": sql
        }
    
    def explain_query(self, query_data):
        """Provide an explanation of the query"""
        entity = query_data.get("entity", "")
        operation = query_data.get("operation", "")
        conditions = query_data.get("conditions", [])
        sql = query_data.get("sql", "")
        
        explanation = {
            "summary": f"This query is looking for {operation} data from the {entity} table.",
            "details": []
        }
        
        if operation == 'select':
            explanation["details"].append("The query will return all columns from the table.")
        elif operation == 'count':
            explanation["details"].append("The query will count the number of rows in the table.")
        elif operation == 'sum':
            if entity == 'sales':
                explanation["details"].append("The query will sum up the total price of all sales.")
            elif entity == 'products':
                explanation["details"].append("The query will calculate the total inventory value.")
        elif operation == 'average':
            if entity == 'sales':
                explanation["details"].append("The query will calculate the average sale price.")
            elif entity == 'products':
                explanation["details"].append("The query will calculate the average product price.")
        elif operation == 'max':
            if entity == 'sales':
                explanation["details"].append("The query will find the highest sale price.")
            elif entity == 'products':
                explanation["details"].append("The query will find the most expensive product.")
        elif operation == 'min':
            if entity == 'sales':
                explanation["details"].append("The query will find the lowest sale price.")
            elif entity == 'products':
                explanation["details"].append("The query will find the cheapest product.")
        
        if conditions:
            explanation["details"].append("The query includes the following conditions:")
            for condition in conditions:
                explanation["details"].append(f"- {condition}")
        
        explanation["sql"] = sql
        
        return explanation
    
    def validate_query(self, query_data):
        """Check if a query is feasible with the current database schema"""
        entity = query_data.get("entity", "")
        operation = query_data.get("operation", "")
        conditions = query_data.get("conditions", [])
        sql = query_data.get("sql", "")
        
        # Check if the entity exists
        valid_entities = list(self.entities.keys())
        if entity not in valid_entities:
            return {
                "valid": False,
                "error": f"Entity '{entity}' does not exist. Valid entities are: {', '.join(valid_entities)}"
            }
        
        # Check if the operation is valid
        valid_operations = list(self.keywords.keys())
        if operation not in valid_operations:
            return {
                "valid": False,
                "error": f"Operation '{operation}' is not supported. Valid operations are: {', '.join(valid_operations)}"
            }
        
        # Try executing the query to see if it works
        try:
            result = execute_query(sql)
            if result is not None:
                return {
                    "valid": True,
                    "message": "The query is valid and can be executed successfully."
                }
            else:
                return {
                    "valid": False,
                    "error": "The query failed to execute. There may be an issue with the SQL syntax."
                }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Error executing query: {str(e)}"
            }
    
    def execute_query(self, query_data):
        """Execute the SQL query and return the results"""
        sql = query_data.get("sql", "")
        
        try:
            result = execute_query(sql)
            if result is not None:
                return {
                    "success": True,
                    "data": result
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to execute query"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing query: {str(e)}"
            }
