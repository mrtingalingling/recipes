// AT Protocol account management and wallet linking
const { createAccount, linkWallet } = require('at-protocol-sdk');

async function handleAccount(user, walletAddress) {
  const account = await createAccount(user);
  if (walletAddress) {
    // Prompt user to link wallet
    const linked = await linkWallet(account, walletAddress);
    return { account, linked };
  }
  return { account };
}

module.exports = { handleAccount };
