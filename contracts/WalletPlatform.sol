// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract WalletPlatform is ReentrancyGuard, Ownable {
    using Counters for Counters.Counter;
    
    Counters.Counter private _connectionIds;
    Counters.Counter private _transactionIds;
    
    struct Connection {
        uint256 id;
        string userId;
        address walletAddress;
        bool isActive;
        uint256 createdAt;
        uint256 expiresAt;
    }
    
    struct Transaction {
        uint256 id;
        uint256 connectionId;
        address from;
        address to;
        uint256 amount;
        bool isConfirmed;
        uint256 createdAt;
        string txHash;
    }
    
    mapping(uint256 => Connection) public connections;
    mapping(uint256 => Transaction) public transactions;
    mapping(address => uint256[]) public userConnections;
    mapping(string => uint256) public userIdToConnection;
    
    event ConnectionCreated(uint256 indexed connectionId, string indexed userId, uint256 expiresAt);
    event ConnectionActivated(uint256 indexed connectionId, address indexed walletAddress);
    event TransactionCreated(uint256 indexed transactionId, uint256 indexed connectionId, address from, address to, uint256 amount);
    event TransactionConfirmed(uint256 indexed transactionId, string txHash);
    
    modifier onlyConnectionOwner(uint256 connectionId) {
        require(connections[connectionId].isActive, "Connection not active");
        require(connections[connectionId].walletAddress == msg.sender, "Not connection owner");
        _;
    }
    
    modifier connectionExists(uint256 connectionId) {
        require(connections[connectionId].id != 0, "Connection does not exist");
        _;
    }
    
    modifier connectionNotExpired(uint256 connectionId) {
        require(block.timestamp < connections[connectionId].expiresAt, "Connection expired");
        _;
    }
    
    function createConnection(string memory userId, uint256 duration) external onlyOwner returns (uint256) {
        require(bytes(userId).length > 0, "User ID cannot be empty");
        require(duration > 0, "Duration must be greater than 0");
        
        _connectionIds.increment();
        uint256 connectionId = _connectionIds.current();
        
        connections[connectionId] = Connection({
            id: connectionId,
            userId: userId,
            walletAddress: address(0),
            isActive: false,
            createdAt: block.timestamp,
            expiresAt: block.timestamp + duration
        });
        
        userIdToConnection[userId] = connectionId;
        
        emit ConnectionCreated(connectionId, userId, connections[connectionId].expiresAt);
        
        return connectionId;
    }
    
    function activateConnection(uint256 connectionId) external connectionExists(connectionId) connectionNotExpired(connectionId) {
        require(!connections[connectionId].isActive, "Connection already active");
        require(connections[connectionId].walletAddress == address(0), "Connection already has wallet");
        
        connections[connectionId].walletAddress = msg.sender;
        connections[connectionId].isActive = true;
        
        userConnections[msg.sender].push(connectionId);
        
        emit ConnectionActivated(connectionId, msg.sender);
    }
    
    function createTransaction(uint256 connectionId, address to, uint256 amount) 
        external 
        onlyConnectionOwner(connectionId) 
        connectionNotExpired(connectionId)
        returns (uint256)
    {
        require(to != address(0), "Invalid recipient address");
        require(amount > 0, "Amount must be greater than 0");
        
        _transactionIds.increment();
        uint256 transactionId = _transactionIds.current();
        
        transactions[transactionId] = Transaction({
            id: transactionId,
            connectionId: connectionId,
            from: msg.sender,
            to: to,
            amount: amount,
            isConfirmed: false,
            createdAt: block.timestamp,
            txHash: ""
        });
        
        emit TransactionCreated(transactionId, connectionId, msg.sender, to, amount);
        
        return transactionId;
    }
    
    function confirmTransaction(uint256 transactionId, string memory txHash) external onlyOwner {
        require(transactions[transactionId].id != 0, "Transaction does not exist");
        require(!transactions[transactionId].isConfirmed, "Transaction already confirmed");
        
        transactions[transactionId].isConfirmed = true;
        transactions[transactionId].txHash = txHash;
        
        emit TransactionConfirmed(transactionId, txHash);
    }
    
    function getConnection(uint256 connectionId) external view returns (Connection memory) {
        return connections[connectionId];
    }
    
    function getTransaction(uint256 transactionId) external view returns (Transaction memory) {
        return transactions[transactionId];
    }
    
    function getUserConnections(address user) external view returns (uint256[] memory) {
        return userConnections[user];
    }
    
    function getConnectionByUserId(string memory userId) external view returns (Connection memory) {
        uint256 connectionId = userIdToConnection[userId];
        return connections[connectionId];
    }
    
    function isConnectionActive(uint256 connectionId) external view returns (bool) {
        return connections[connectionId].isActive && 
               block.timestamp < connections[connectionId].expiresAt;
    }
    
    function getConnectionCount() external view returns (uint256) {
        return _connectionIds.current();
    }
    
    function getTransactionCount() external view returns (uint256) {
        return _transactionIds.current();
    }
    
    // Emergency functions for owner
    function extendConnection(uint256 connectionId, uint256 additionalTime) external onlyOwner {
        require(connections[connectionId].id != 0, "Connection does not exist");
        connections[connectionId].expiresAt += additionalTime;
    }
    
    function deactivateConnection(uint256 connectionId) external onlyOwner {
        require(connections[connectionId].id != 0, "Connection does not exist");
        connections[connectionId].isActive = false;
    }
    
    function withdrawFees() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
} 