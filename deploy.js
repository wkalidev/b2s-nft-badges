require('dotenv').config();
const { makeContractDeploy, AnchorMode } = require('@stacks/transactions');
const { StacksMainnet } = require('@stacks/network');
const { generateWallet } = require('@stacks/wallet-sdk');
const fs = require('fs');

const API = 'https://api.hiro.so';
const CONTRACTS = [
  //{ name: 'b2s-badges',      path: './contracts/b2s-badges.clar' },
  { name: 'b2s-marketplace', path: './contracts/b2s-marketplace.clar' },
];

function readContract(filePath) {
  return fs.readFileSync(filePath, { encoding: 'ascii' })
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .replace(/[^\x20-\x7E\n\t]/g, '')
    .trim();
}

async function deployContract(name, path, senderKey, network) {
  console.log(`\nDeploying ${name}...`);
  const tx = await makeContractDeploy({
    contractName: name,
    codeBody: readContract(path),
    senderKey,
    network,
    anchorMode: AnchorMode.Any,
    fee: 100_000n,
  });
  const res = await fetch(`${API}/v2/transactions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: tx.serialize(),
  });
  const body = await res.text();
  if (!res.ok) throw new Error(`Broadcast failed (${res.status}): ${body}`);
  console.log(`✅ ${name}: ${body.replace(/"/g, '')}`);
}

async function main() {
  const mnemonic = process.env.MNEMONIC;
  if (!mnemonic) throw new Error('MNEMONIC not set in .env');
  const wallet = await generateWallet({ secretKey: mnemonic, password: '' });
  const senderKey = wallet.accounts[0].stxPrivateKey;
  const network = new StacksMainnet({ url: API });
  for (const c of CONTRACTS) {
    try { await deployContract(c.name, c.path, senderKey, network); }
    catch (err) { console.error(`❌ ${c.name}: ${err.message}`); }
  }
}

main().catch(console.error);