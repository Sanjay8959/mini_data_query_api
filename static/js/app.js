// Global variables
let authToken = '';
let currentQuery = '';

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Auth elements
    const loginBtn = document.getElementById('login-btn');
    const authStatus = document.getElementById('auth-status');
    const authSection = document.getElementById('auth-section');
    const querySection = document.getElementById('query-section');
    const resultsSection = document.getElementById('results-section');
    
    // Query elements
    const queryInput = document.getElementById('query-input');
    const queryBtn = document.getElementById('query-btn');
    const exampleQueries = document.querySelectorAll('.example-query');
    
    // Results elements
    const resultsContainer = document.getElementById('results-container');
    const explanationContainer = document.getElementById('explanation-container');
    const validationContainer = document.getElementById('validation-container');
    const sqlContainer = document.getElementById('sql-container');
    
    // Tab elements
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    // Event Listeners
    loginBtn.addEventListener('click', handleLogin);
    queryBtn.addEventListener('click', handleQuery);
    
    // Example query click events
    exampleQueries.forEach(query => {
        query.addEventListener('click', function(e) {
            e.preventDefault();
            queryInput.value = this.textContent;
        });
    });
    
    // Tab click events
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and panes
            tabBtns.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to current button and pane
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Login function
    async function handleLogin() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        if (!username || !password) {
            showAuthStatus('Please enter both username and password', false);
            return;
        }
        
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                authToken = data.token;
                showAuthStatus('Login successful!', true);
                
                // Show query section
                authSection.style.display = 'none';
                querySection.style.display = 'block';
            } else {
                showAuthStatus(`Login failed: ${data.error}`, false);
            }
        } catch (error) {
            showAuthStatus(`Error: ${error.message}`, false);
        }
    }
    
    // Query function
    async function handleQuery() {
        const query = queryInput.value;
        
        if (!query) {
            alert('Please enter a query');
            return;
        }
        
        if (!authToken) {
            alert('Please login first');
            return;
        }
        
        currentQuery = query;
        
        // Show results section
        resultsSection.style.display = 'block';
        
        // Process query
        await processQuery(query);
        
        // Get explanation
        await explainQuery(query);
        
        // Validate query
        await validateQuery(query);
    }
    
    // Process query
    async function processQuery(query) {
        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Display SQL
                sqlContainer.innerHTML = `<div class="sql-code">${data.parsed_query.sql}</div>`;
                
                // Display results
                displayResults(data.results.data);
            } else {
                resultsContainer.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            }
        } catch (error) {
            resultsContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }
    
    // Explain query
    async function explainQuery(query) {
        try {
            const response = await fetch('/explain', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Display explanation
                let explanationHTML = `<p>${data.explanation.explanation.summary}</p><ul>`;
                
                data.explanation.explanation.details.forEach(detail => {
                    explanationHTML += `<li class="explanation-item">${detail}</li>`;
                });
                
                explanationHTML += '</ul>';
                explanationContainer.innerHTML = explanationHTML;
            } else {
                explanationContainer.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            }
        } catch (error) {
            explanationContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }
    
    // Validate query
    async function validateQuery(query) {
        try {
            const response = await fetch('/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Display validation
                const validationResult = data.validation.validation;
                const validClass = validationResult.valid ? 'valid' : 'invalid';
                const message = validationResult.valid ? validationResult.message : validationResult.error;
                
                validationContainer.innerHTML = `
                    <div class="validation-result ${validClass}">
                        <p><strong>${validationResult.valid ? 'Valid' : 'Invalid'}</strong>: ${message}</p>
                    </div>
                `;
            } else {
                validationContainer.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            }
        } catch (error) {
            validationContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }
    
    // Helper function to display results
    function displayResults(results) {
        if (!results || results.length === 0) {
            resultsContainer.innerHTML = '<p>No results found</p>';
            return;
        }
        
        // Check if results is an array of objects
        if (Array.isArray(results) && typeof results[0] === 'object') {
            // Create table
            let tableHTML = '<table class="results-table"><thead><tr>';
            
            // Get headers from first object
            const headers = Object.keys(results[0]);
            headers.forEach(header => {
                tableHTML += `<th>${header}</th>`;
            });
            
            tableHTML += '</tr></thead><tbody>';
            
            // Add rows
            results.forEach(row => {
                tableHTML += '<tr>';
                headers.forEach(header => {
                    tableHTML += `<td>${row[header]}</td>`;
                });
                tableHTML += '</tr>';
            });
            
            tableHTML += '</tbody></table>';
            resultsContainer.innerHTML = tableHTML;
        } else {
            // Simple display for non-tabular data
            resultsContainer.innerHTML = `<pre>${JSON.stringify(results, null, 2)}</pre>`;
        }
    }
    
    // Helper function to show auth status
    function showAuthStatus(message, isSuccess) {
        authStatus.textContent = message;
        authStatus.className = 'auth-status';
        
        if (isSuccess) {
            authStatus.classList.add('success');
        } else {
            authStatus.classList.add('error');
        }
    }
});
