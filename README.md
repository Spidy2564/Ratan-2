# Wallet Connection Platform

A modern Web3 platform that allows you to create wallet connection links and perform transactions. Users can connect their wallets through a simple link and you can manage their connections and transactions.

## Features

- **Wallet Connection Links**: Generate unique links for users to connect their wallets
- **MetaMask Integration**: Seamless connection with MetaMask wallet
- **Transaction Management**: Perform and track transactions from connected wallets
- **Admin Dashboard**: Monitor connections and transactions
- **Smart Contract Integration**: On-chain connection and transaction tracking
- **Modern UI**: Beautiful, responsive interface with glass morphism effects

## Project Structure

```
wallet-platform/
├── frontend/                 # Frontend application
│   ├── index.html           # Main wallet connection interface
│   └── app.js              # Frontend JavaScript logic
├── backend/                 # Flask backend server
│   ├── server.py           # Main server application
│   ├── requirements.txt    # Python dependencies
│   └── templates/          # HTML templates
│       ├── connect.html    # Connection page for users
│       └── admin.html      # Admin dashboard
└── contracts/              # Smart contracts
    ├── WalletPlatform.sol  # Main smart contract
    ├── deploy.js           # Deployment script
    ├── hardhat.config.js   # Hardhat configuration
    └── package.json        # Node.js dependencies
```

## Quick Start

### 1. Backend Setup

```bash
cd wallet-platform/backend
pip install -r requirements.txt
python server.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

Simply open `wallet-platform/frontend/index.html` in your browser, or serve it using a local server:

```bash
cd wallet-platform/frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

### 3. Smart Contract Setup (Optional)

```bash
cd wallet-platform/contracts
npm install
npx hardhat compile
npx hardhat node  # Start local blockchain
npx hardhat run deploy.js --network localhost
```

## How It Works

### 1. Creating Connection Links

1. Go to the admin dashboard at `http://localhost:5000/admin`
2. Enter a user ID and optional metadata
3. Click "Generate Connection Link"
4. Copy the generated link and share it with the user

### 2. User Connection Process

1. User clicks on your connection link
2. They see a beautiful wallet connection page
3. They choose MetaMask or WalletConnect
4. After connecting, their wallet address is stored
5. You can now perform transactions from their wallet

### 3. Performing Transactions

1. Once a wallet is connected, you can send transactions
2. Enter recipient address and amount
3. Transaction is executed through the connected wallet
4. Transaction history is maintained locally

## API Endpoints

### Connection Management
- `POST /api/connect` - Create new connection
- `GET /api/connections/<id>` - Get connection status
- `POST /api/connections/<id>/update` - Update connection with wallet info

### Transaction Management
- `POST /api/transactions` - Create transaction request
- `GET /api/transactions/<id>` - Get transaction status
- `POST /api/transactions/<id>/update` - Update transaction

### Statistics
- `GET /api/stats` - Get platform statistics

## Smart Contract Features

The `WalletPlatform.sol` contract provides:

- **Connection Management**: Create and manage wallet connections
- **Transaction Tracking**: Record and confirm transactions
- **Access Control**: Only connection owners can perform transactions
- **Expiration System**: Connections expire after a set time
- **Event Logging**: All actions are logged as events

## Security Features

- **Connection Expiration**: Links expire after 1 hour by default
- **Wallet Verification**: Only connected wallets can perform transactions
- **Transaction Validation**: All transactions are validated before execution
- **Access Control**: Admin-only functions for platform management

## Customization

### Changing Connection Expiry Time

In `backend/server.py`, modify the expiry calculation:

```python
'expires_at': (datetime.now().timestamp() + 3600),  # 1 hour
```

### Adding New Wallet Types

1. Add wallet type to the frontend UI
2. Implement connection logic in `app.js`
3. Update the connection page template

### Styling

The platform uses Tailwind CSS with custom glass morphism effects. Modify the CSS classes in the HTML files to change the appearance.

## Deployment

### Backend Deployment

1. Set up a Python environment
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Deploy to your preferred hosting service

### Frontend Deployment

The frontend is static and can be deployed to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

### Smart Contract Deployment

1. Set up environment variables in `.env`:
   ```
   PRIVATE_KEY=your_private_key
   SEPOLIA_URL=your_sepolia_rpc_url
   MAINNET_URL=your_mainnet_rpc_url
   ```

2. Deploy to your preferred network:
   ```bash
   npx hardhat run deploy.js --network sepolia
   ```

## Troubleshooting

### Common Issues

1. **MetaMask not detected**: Ensure MetaMask is installed and unlocked
2. **Connection failed**: Check if the connection link is still valid
3. **Transaction failed**: Verify the wallet has sufficient funds
4. **Backend not starting**: Check if port 5000 is available

### Debug Mode

Enable debug mode in the backend by setting:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

---

**Note**: This platform is for educational and development purposes. Always test thoroughly before using in production environments. 