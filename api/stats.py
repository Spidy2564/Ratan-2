from http.server import BaseHTTPRequestHandler
import json
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request for platform statistics"""
        try:
            # Load database
            db = load_database()
            
            # Calculate statistics
            total_connections = len(db['connections'])
            active_connections = len([c for c in db['connections'] if c['status'] == 'connected'])
            total_transactions = len(db['transactions'])
            successful_transactions = len([t for t in db['transactions'] if t.get('status') == 'confirmed'])
            
            stats = {
                'success': True,
                'stats': {
                    'total_connections': total_connections,
                    'active_connections': active_connections,
                    'total_transactions': total_transactions,
                    'successful_transactions': successful_transactions,
                    'success_rate': (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0
                }
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(stats).encode())
            
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
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
