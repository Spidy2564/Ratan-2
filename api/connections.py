from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime

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
    def do_GET(self):
        """Handle GET request for connection status"""
        try:
            # Extract connection ID from path
            path_parts = self.path.split('/')
            if len(path_parts) < 4:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid connection ID'}).encode())
                return
            
            connection_id = path_parts[3]
            
            # Load database and find connection
            db = load_database()
            connection = None
            
            for conn in db['connections']:
                if conn['id'] == connection_id:
                    connection = conn
                    break
            
            if not connection:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Connection not found'}).encode())
                return
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(connection).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_POST(self):
        """Handle POST request for updating connections"""
        try:
            # Extract connection ID from path
            path_parts = self.path.split('/')
            if len(path_parts) < 4:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid connection ID'}).encode())
                return
            
            connection_id = path_parts[3]
            
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Load database and find connection
            db = load_database()
            connection = None
            connection_index = -1
            
            for i, conn in enumerate(db['connections']):
                if conn['id'] == connection_id:
                    connection = conn
                    connection_index = i
                    break
            
            if not connection:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Connection not found'}).encode())
                return
            
            # Update connection
            db['connections'][connection_index].update(data)
            db['connections'][connection_index]['updated_at'] = datetime.now().isoformat()
            save_database(db)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response = {
                'success': True,
                'connection': db['connections'][connection_index]
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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
