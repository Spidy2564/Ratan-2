#!/usr/bin/env python3
"""
Example Usage of Wallet Platform
This script demonstrates how to use the wallet platform programmatically.
"""

import requests
import json
import time
from datetime import datetime

class WalletPlatformClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        
    def create_connection(self, user_id, metadata=None):
        """Create a new wallet connection"""
        url = f"{self.base_url}/api/connect"
        data = {
            "user_id": user_id,
            "metadata": metadata or {}
        }
        
        response = requests.post(url, json=data)
        return response.json()
    
    def get_connection(self, connection_id):
        """Get connection status"""
        url = f"{self.base_url}/api/connections/{connection_id}"
        response = requests.get(url)
        return response.json()
    
    def update_connection(self, connection_id, wallet_address, network="ethereum"):
        """Update connection with wallet info"""
        url = f"{self.base_url}/api/connections/{connection_id}/update"
        data = {
            "wallet_address": wallet_address,
            "network": network
        }
        
        response = requests.post(url, json=data)
        return response.json()
    
    def create_transaction(self, connection_id, to_address, amount):
        """Create a transaction request"""
        url = f"{self.base_url}/api/transactions"
        data = {
            "connection_id": connection_id,
            "to_address": to_address,
            "amount": amount
        }
        
        response = requests.post(url, json=data)
        return response.json()
    
    def get_transaction(self, transaction_id):
        """Get transaction status"""
        url = f"{self.base_url}/api/transactions/{transaction_id}"
        response = requests.get(url)
        return response.json()
    
    def get_stats(self):
        """Get platform statistics"""
        url = f"{self.base_url}/api/stats"
        response = requests.get(url)
        return response.json()

def main():
    """Example usage of the wallet platform"""
    print("🔗 Wallet Platform Example Usage")
    print("=" * 50)
    
    # Initialize client
    client = WalletPlatformClient()
    
    try:
        # Check if server is running
        stats = client.get_stats()
        print("✅ Server is running")
        print(f"📊 Platform stats: {stats}")
        
        # Example 1: Create a connection for a user
        print("\n📝 Example 1: Creating a connection")
        user_id = "user_123"
        metadata = {"source": "telegram", "username": "@example_user"}
        
        connection_result = client.create_connection(user_id, metadata)
        print(f"Connection created: {json.dumps(connection_result, indent=2)}")
        
        connection_id = connection_result['connection_id']
        connection_link = connection_result['connection_link']
        
        print(f"🔗 Connection link: {connection_link}")
        print(f"⏰ Expires at: {datetime.fromtimestamp(connection_result['expires_at'])}")
        
        # Example 2: Check connection status
        print("\n📊 Example 2: Checking connection status")
        connection_status = client.get_connection(connection_id)
        print(f"Connection status: {json.dumps(connection_status, indent=2)}")
        
        # Example 3: Simulate wallet connection (in real scenario, user would connect via frontend)
        print("\n💼 Example 3: Simulating wallet connection")
        wallet_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        
        update_result = client.update_connection(connection_id, wallet_address, "ethereum")
        print(f"Connection updated: {json.dumps(update_result, indent=2)}")
        
        # Example 4: Create a transaction
        print("\n💰 Example 4: Creating a transaction")
        to_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        amount = 0.001
        
        transaction_result = client.create_transaction(connection_id, to_address, amount)
        print(f"Transaction created: {json.dumps(transaction_result, indent=2)}")
        
        transaction_id = transaction_result['transaction_id']
        
        # Example 5: Check transaction status
        print("\n📈 Example 5: Checking transaction status")
        transaction_status = client.get_transaction(transaction_id)
        print(f"Transaction status: {json.dumps(transaction_status, indent=2)}")
        
        # Example 6: Get updated platform stats
        print("\n📊 Example 6: Updated platform statistics")
        updated_stats = client.get_stats()
        print(f"Updated stats: {json.dumps(updated_stats, indent=2)}")
        
        print("\n✅ All examples completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the backend server is running at http://localhost:5000")
        print("Run: python start.py to start the platform")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demonstrate_telegram_integration():
    """Demonstrate how to integrate with Telegram"""
    print("\n📱 Telegram Integration Example")
    print("=" * 40)
    
    client = WalletPlatformClient()
    
    # Simulate creating connections for Telegram users
    telegram_users = [
        {"user_id": "telegram_user_1", "username": "@crypto_trader_1"},
        {"user_id": "telegram_user_2", "username": "@defi_enthusiast"},
        {"user_id": "telegram_user_3", "username": "@nft_collector"}
    ]
    
    connections = []
    
    for user in telegram_users:
        metadata = {
            "source": "telegram",
            "username": user["username"],
            "created_via": "bot"
        }
        
        try:
            result = client.create_connection(user["user_id"], metadata)
            connections.append({
                "user": user,
                "connection_id": result["connection_id"],
                "link": result["connection_link"]
            })
            
            print(f"✅ Created connection for {user['username']}")
            print(f"   Link: {result['connection_link']}")
            
        except Exception as e:
            print(f"❌ Failed to create connection for {user['username']}: {e}")
    
    print(f"\n📊 Created {len(connections)} connections for Telegram users")
    
    return connections

if __name__ == "__main__":
    # Run basic examples
    main()
    
    # Run Telegram integration example
    demonstrate_telegram_integration()
    
    print("\n🎉 Example usage completed!")
    print("\n💡 Tips:")
    print("- Use the admin dashboard to monitor connections")
    print("- Share connection links with users via Telegram")
    print("- Track transaction status in real-time")
    print("- Integrate with your existing bot or application") 