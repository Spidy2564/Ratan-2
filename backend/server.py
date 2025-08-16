from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime
import secrets
import hashlib

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE_FILE'] = 'wallet_connections.json'

# Database to store connection requests
def load_database():
    if os.path.exists(app.config['DATABASE_FILE']):
        with open(app.config['DATABASE_FILE'], 'r') as f:
            return json.load(f)
    return {'connections': [], 'transactions': []}

def save_database(data):
    with open(app.config['DATABASE_FILE'], 'w') as f:
        json.dump(data, f, indent=2)

# Routes
@app.route('/')
def index():
    return render_template('connect.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/connect', methods=['POST'])
def create_connection():
    """Create a new wallet connection request"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({'error': 'user_id is required'}), 400
        
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
        connection_link = f"{request.host_url}connect/{connection_id}"
        
        return jsonify({
            'success': True,
            'connection_id': connection_id,
            'connection_link': connection_link,
            'expires_at': connection_request['expires_at']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/connect/<connection_id>')
def connect_page(connection_id):
    """Connection page for users"""
    return render_template('connect.html')

@app.route('/mobile/<connection_id>')
def mobile_page(connection_id):
    """Mobile-optimized connection page"""
    return render_template('mobile.html')

@app.route('/api/connections/<connection_id>')
def get_connection(connection_id):
    """Get connection status"""
    try:
        db = load_database()
        
        for connection in db['connections']:
            if connection['id'] == connection_id:
                return jsonify(connection)
        
        return jsonify({'error': 'Connection not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections/<connection_id>/update', methods=['POST'])
def update_connection(connection_id):
    """Update connection with wallet info"""
    try:
        data = request.get_json()
        
        if not data or 'wallet_address' not in data:
            return jsonify({'error': 'wallet_address is required'}), 400
        
        db = load_database()
        
        for connection in db['connections']:
            if connection['id'] == connection_id:
                connection['wallet_address'] = data['wallet_address']
                connection['network'] = data.get('network', 'ethereum')
                connection['status'] = 'connected'
                connection['connected_at'] = datetime.now().isoformat()
                save_database(db)
                
                return jsonify({'success': True, 'connection': connection})
        
        return jsonify({'error': 'Connection not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections')
def get_all_connections():
    """Get all connections"""
    try:
        db = load_database()
        return jsonify(db['connections'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction request"""
    try:
        data = request.get_json()
        
        required_fields = ['connection_id', 'to_address', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Verify connection exists and is active
        db = load_database()
        connection = None
        for conn in db['connections']:
            if conn['id'] == data['connection_id'] and conn['status'] == 'connected':
                connection = conn
                break
        
        if not connection:
            return jsonify({'error': 'Invalid or inactive connection'}), 400
        
        # Create transaction request
        transaction = {
            'id': secrets.token_urlsafe(32),
            'connection_id': data['connection_id'],
            'from_address': connection['wallet_address'],
            'to_address': data['to_address'],
            'amount': data['amount'],
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'hash': None,
            'gas_used': None,
            'gas_price': None
        }
        
        db['transactions'].append(transaction)
        save_database(db)
        
        return jsonify({
            'success': True,
            'transaction_id': transaction['id'],
            'transaction': transaction
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/<transaction_id>')
def get_transaction(transaction_id):
    """Get transaction status"""
    try:
        db = load_database()
        
        for transaction in db['transactions']:
            if transaction['id'] == transaction_id:
                return jsonify(transaction)
        
        return jsonify({'error': 'Transaction not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/<transaction_id>/update', methods=['POST'])
def update_transaction(transaction_id):
    """Update transaction with blockchain info"""
    try:
        data = request.get_json()
        
        db = load_database()
        
        for transaction in db['transactions']:
            if transaction['id'] == transaction_id:
                transaction.update(data)
                transaction['updated_at'] = datetime.now().isoformat()
                save_database(db)
                
                return jsonify({'success': True, 'transaction': transaction})
        
        return jsonify({'error': 'Transaction not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections/<connection_id>/transactions')
def get_connection_transactions(connection_id):
    """Get all transactions for a connection"""
    try:
        db = load_database()
        
        transactions = [
            tx for tx in db['transactions'] 
            if tx['connection_id'] == connection_id
        ]
        
        return jsonify({
            'success': True,
            'transactions': transactions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions')
def get_all_transactions():
    """Get all transactions"""
    try:
        db = load_database()
        return jsonify(db['transactions'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get platform statistics"""
    try:
        db = load_database()
        
        total_connections = len(db['connections'])
        active_connections = len([c for c in db['connections'] if c['status'] == 'connected'])
        total_transactions = len(db['transactions'])
        successful_transactions = len([t for t in db['transactions'] if t['status'] == 'confirmed'])
        
        return jsonify({
            'success': True,
            'stats': {
                'total_connections': total_connections,
                'active_connections': active_connections,
                'total_transactions': total_transactions,
                'successful_transactions': successful_transactions,
                'success_rate': (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 