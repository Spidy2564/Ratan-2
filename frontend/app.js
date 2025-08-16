// Global variables
let provider = null;
let signer = null;
let connectedAddress = null;
let transactionHistory = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function () {
    checkWalletConnection();
    loadTransactionHistory();
});

// Check if wallet is already connected
async function checkWalletConnection() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_accounts' });
            if (accounts.length > 0) {
                await connectWallet('metamask');
            }
        } catch (error) {
            console.log('No wallet connected');
        }
    }
}

// Connect wallet function
async function connectWallet(walletType) {
    showLoading('Connecting wallet...');

    try {
        if (walletType === 'metamask') {
            await connectMetaMask();
        } else if (walletType === 'walletconnect') {
            await connectWalletConnect();
        }
    } catch (error) {
        hideLoading();
        showError('Failed to connect wallet: ' + error.message);
    }
}

// Connect to MetaMask
async function connectMetaMask() {
    if (typeof window.ethereum === 'undefined') {
        throw new Error('MetaMask is not installed. Please install MetaMask extension.');
    }

    try {
        // Request account access
        const accounts = await window.ethereum.request({
            method: 'eth_requestAccounts'
        });

        if (accounts.length === 0) {
            throw new Error('No accounts found');
        }

        // Create provider and signer
        provider = new ethers.providers.Web3Provider(window.ethereum);
        signer = provider.getSigner();
        connectedAddress = accounts[0];

        // Get network info
        const network = await provider.getNetwork();

        hideLoading();
        updateConnectionStatus(true, connectedAddress, network.name);
        showTransactionSection();

        // Listen for account changes
        window.ethereum.on('accountsChanged', handleAccountsChanged);
        window.ethereum.on('chainChanged', handleChainChanged);

        showSuccess('Wallet connected successfully!');

    } catch (error) {
        throw new Error('Failed to connect to MetaMask: ' + error.message);
    }
}

// Connect to WalletConnect
async function connectWalletConnect() {
    try {
        // Check if WalletConnect is loaded
        if (typeof WalletConnectProvider === 'undefined') {
            throw new Error('WalletConnect library not loaded. Please refresh the page and try again.');
        }

        // Wait a bit for the library to be fully initialized
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Initialize WalletConnect with simpler configuration
        const provider = await WalletConnectProvider.default.init({
            rpc: {
                1: 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', // Ethereum mainnet
            },
            qrcode: true,
            pollingInterval: 12000,
        });

        // Enable session (triggers QR Code modal)
        await provider.enable();

        // Create ethers provider
        const ethersProvider = new ethers.providers.Web3Provider(provider);

        // Show fallback URI if QR code doesn't work
        if (provider.connector && provider.connector.uri) {
            console.log('WalletConnect URI:', provider.connector.uri);
            // Display URI as fallback
            showWalletConnectFallback(provider.connector.uri);
        }
        const signer = ethersProvider.getSigner();

        // Get connected address
        const accounts = await ethersProvider.listAccounts();
        if (accounts.length === 0) {
            throw new Error('No accounts found');
        }

        // Update global variables
        window.provider = ethersProvider;
        window.signer = signer;
        window.connectedAddress = accounts[0];

        // Get network info
        const network = await ethersProvider.getNetwork();

        hideLoading();
        updateConnectionStatus(true, connectedAddress, network.name);
        showTransactionSection();

        showSuccess('WalletConnect connected successfully!');

        // Listen for disconnect
        provider.on('disconnect', () => {
            disconnectWallet();
        });

    } catch (error) {
        hideLoading();
        showError('Failed to connect WalletConnect: ' + error.message);
    }
}

// Handle account changes
async function handleAccountsChanged(accounts) {
    if (accounts.length === 0) {
        // User disconnected wallet
        disconnectWallet();
    } else {
        // User switched accounts
        connectedAddress = accounts[0];
        signer = provider.getSigner();
        updateConnectionStatus(true, connectedAddress);
    }
}

// Handle chain changes
async function handleChainChanged(chainId) {
    window.location.reload();
}

// Disconnect wallet
function disconnectWallet() {
    provider = null;
    signer = null;
    connectedAddress = null;
    updateConnectionStatus(false);
    hideTransactionSection();
    showSuccess('Wallet disconnected');
}

// Update connection status UI
function updateConnectionStatus(connected, address = '', network = '') {
    const statusDiv = document.getElementById('connectionStatus');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');
    const walletInfo = document.getElementById('walletInfo');

    if (connected) {
        statusDiv.classList.remove('hidden');
        statusIcon.className = 'w-8 h-8 rounded-full mr-3 bg-green-500 flex items-center justify-center';
        statusIcon.innerHTML = '<i class="fas fa-check text-white"></i>';
        statusText.textContent = 'Wallet Connected';
        walletInfo.innerHTML = `
            <div class="space-y-2">
                <p><strong>Address:</strong> ${address}</p>
                <p><strong>Network:</strong> ${network}</p>
                <button onclick="disconnectWallet()" 
                        class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm">
                    <i class="fas fa-times mr-1"></i>Disconnect
                </button>
            </div>
        `;
    } else {
        statusDiv.classList.add('hidden');
    }
}

// Show transaction section
function showTransactionSection() {
    document.getElementById('transactionSection').classList.remove('hidden');
    document.getElementById('transactionHistory').classList.remove('hidden');
}

// Hide transaction section
function hideTransactionSection() {
    document.getElementById('transactionSection').classList.add('hidden');
    document.getElementById('transactionHistory').classList.add('hidden');
}

// Send transaction
async function sendTransaction() {
    const recipientAddress = document.getElementById('recipientAddress').value.trim();
    const amount = document.getElementById('amount').value;

    // Validate inputs
    if (!recipientAddress) {
        showError('Please enter recipient address');
        return;
    }
    if (!ethers.utils.isAddress(recipientAddress)) {
        showError('Invalid recipient address');
        return;
    }
    if (!amount || amount <= 0) {
        showError('Please enter a valid amount');
        return;
    }

    if (!signer) {
        showError('Please connect your wallet first');
        return;
    }

    showLoading('Sending transaction...');

    try {
        // Convert amount to wei
        const amountWei = ethers.utils.parseEther(amount);

        // Get current gas price
        const gasPrice = await provider.getGasPrice();

        // Estimate gas
        const gasEstimate = await provider.estimateGas({
            to: recipientAddress,
            value: amountWei
        });

        // Create transaction
        const tx = {
            to: recipientAddress,
            value: amountWei,
            gasLimit: gasEstimate.mul(120).div(100), // Add 20% buffer
            gasPrice: gasPrice
        };

        // Send transaction
        const transaction = await signer.sendTransaction(tx);

        hideLoading();
        showSuccess(`Transaction sent! Hash: ${transaction.hash}`);

        // Add to history
        addToHistory({
            hash: transaction.hash,
            to: recipientAddress,
            amount: amount,
            timestamp: new Date().toISOString(),
            status: 'pending'
        });

        // Wait for confirmation
        await transaction.wait();

        // Update history status
        updateHistoryStatus(transaction.hash, 'confirmed');
        showSuccess('Transaction confirmed!');

        // Clear form
        document.getElementById('recipientAddress').value = '';
        document.getElementById('amount').value = '';

    } catch (error) {
        hideLoading();
        showError('Transaction failed: ' + error.message);
    }
}

// Add transaction to history
function addToHistory(transaction) {
    transactionHistory.unshift(transaction);
    localStorage.setItem('transactionHistory', JSON.stringify(transactionHistory));
    displayTransactionHistory();
}

// Update transaction status in history
function updateHistoryStatus(hash, status) {
    const transaction = transactionHistory.find(tx => tx.hash === hash);
    if (transaction) {
        transaction.status = status;
        localStorage.setItem('transactionHistory', JSON.stringify(transactionHistory));
        displayTransactionHistory();
    }
}

// Load transaction history from localStorage
function loadTransactionHistory() {
    const saved = localStorage.getItem('transactionHistory');
    if (saved) {
        transactionHistory = JSON.parse(saved);
        displayTransactionHistory();
    }
}

// Display transaction history
function displayTransactionHistory() {
    const historyList = document.getElementById('historyList');

    if (transactionHistory.length === 0) {
        historyList.innerHTML = '<p class="text-white/60 text-center">No transactions yet</p>';
        return;
    }

    historyList.innerHTML = transactionHistory.map(tx => `
        <div class="glass-effect rounded-lg p-4">
            <div class="flex justify-between items-start">
                <div>
                    <p class="text-white font-semibold">To: ${tx.to.substring(0, 6)}...${tx.to.substring(tx.to.length - 4)}</p>
                    <p class="text-white/70 text-sm">Amount: ${tx.amount} ETH</p>
                    <p class="text-white/50 text-xs">${new Date(tx.timestamp).toLocaleString()}</p>
                </div>
                <div class="text-right">
                    <span class="px-2 py-1 rounded text-xs font-semibold ${tx.status === 'confirmed' ? 'bg-green-500 text-white' :
            tx.status === 'pending' ? 'bg-yellow-500 text-white' :
                'bg-red-500 text-white'
        }">
                        ${tx.status}
                    </span>
                    <p class="text-white/50 text-xs mt-1">${tx.hash.substring(0, 10)}...</p>
                </div>
            </div>
        </div>
    `).join('');
}

// UI Helper functions
function showLoading(message) {
    document.getElementById('loadingText').textContent = message;
    document.getElementById('loadingModal').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingModal').classList.add('hidden');
}

function showSuccess(message) {
    document.getElementById('successMessage').textContent = message;
    document.getElementById('successModal').classList.remove('hidden');
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorModal').classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Show WalletConnect fallback URI
function showWalletConnectFallback(uri) {
    const fallbackDiv = document.getElementById('walletConnectFallback');
    const uriInput = document.getElementById('walletConnectUri');

    fallbackDiv.classList.remove('hidden');
    uriInput.value = uri;

    showSuccess('QR Code generated! If scanning fails, copy the URI below to your mobile wallet.');
}

// Copy WalletConnect URI to clipboard
function copyWalletConnectUri() {
    const uriInput = document.getElementById('walletConnectUri');
    uriInput.select();
    document.execCommand('copy');
    showSuccess('URI copied to clipboard!');
}

// Export functions for global access
window.connectWallet = connectWallet;
window.sendTransaction = sendTransaction;
window.closeModal = closeModal;
window.copyWalletConnectUri = copyWalletConnectUri; 