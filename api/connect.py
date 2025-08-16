from http.server import BaseHTTPRequestHandler
import json
import secrets
from datetime import datetime
import os

def load_database():
    """Load database from file"""
    try:
        if os.path.exists('wallet_connections.json'):
            with open('wallet_connections.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return {'connections': [], 'transactions': []}

def save_database(data):
    """Save database to file"""
    try:
        with open('wallet_connections.json', 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for creating connections"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validate input
            if not data or 'user_id' not in data:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'user_id is required'}).encode())
                return
            
            # Generate unique connection ID
            connection_id = secrets.token_urlsafe(32)
            
            # Create connection request
            connection_request = {
                'id': connection_id,
                'user_id': data['user_id'],
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'wallet_address': None,
                'network': None,
                'expires_at': (datetime.now().timestamp() + 3600),  # 1 hour expiry
                'metadata': data.get('metadata', {})
            }
            
            # Save to database
            db = load_database()
            db['connections'].append(connection_request)
            save_database(db)
            
            # Generate connection link
            host = self.headers.get('Host', 'localhost')
            connection_link = f"https://{host}/connect/{connection_id}"
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response = {
                'success': True,
                'connection_id': connection_id,
                'connection_link': connection_link,
                'expires_at': connection_request['expires_at']
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_OPTIONS(self):
        """Handle preflight request"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
