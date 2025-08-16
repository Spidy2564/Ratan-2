const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying WalletPlatform contract...");

  // Get the contract factory
  const WalletPlatform = await ethers.getContractFactory("WalletPlatform");

  // Deploy the contract
  const walletPlatform = await WalletPlatform.deploy();

  // Wait for deployment to finish
  await walletPlatform.deployed();

  console.log("WalletPlatform deployed to:", walletPlatform.address);
  console.log("Contract owner:", await walletPlatform.owner());

  // Verify the deployment
  console.log("\nVerifying deployment...");
  console.log("Connection count:", await walletPlatform.getConnectionCount());
  console.log("Transaction count:", await walletPlatform.getTransactionCount());

  return walletPlatform;
}

// Handle errors
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 