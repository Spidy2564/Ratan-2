# Quick Start Guide

## Option 1: Automatic Startup (Recommended)

```bash
python start.py
```

This will automatically:
- Install dependencies
- Start backend server
- Start frontend server
- Open browsers

## Option 2: Manual Startup

### Start Backend Server

**Windows:**
```bash
cd backend
python server.py
```

**Or use the batch file:**
```bash
run_backend.bat
```

### Start Frontend Server

**Windows:**
```bash
cd frontend
python -m http.server 8000
```

**Or use the batch file:**
```bash
run_frontend.bat
```

## Access the Platform

1. **Backend API**: http://localhost:5000
2. **Admin Dashboard**: http://localhost:5000/admin
3. **Frontend**: http://localhost:8000

## First Steps

1. Open the admin dashboard: http://localhost:5000/admin
2. Create a connection link for a user
3. Share the link with them
4. User connects their wallet
5. Monitor connections and transactions

## Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Install dependencies: `pip install -r backend/requirements.txt`

### Frontend won't start
- Check if port 8000 is available
- Make sure you're in the frontend directory

### Connection issues
- Make sure both servers are running
- Check browser console for errors
- Ensure MetaMask is installed and unlocked 