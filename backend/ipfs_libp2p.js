// IPFS/libp2p integration for decentralized storage
const IPFS = require('ipfs-core');

async function storeData(data) {
  const ipfs = await IPFS.create();
  const { cid } = await ipfs.add(JSON.stringify(data));
  await ipfs.stop();
  return cid.toString();
}

async function fetchData(cid) {
  const ipfs = await IPFS.create();
  const stream = ipfs.cat(cid);
  let data = '';
  for await (const chunk of stream) {
    data += chunk.toString();
  }
  await ipfs.stop();
  return JSON.parse(data);
}

module.exports = { storeData, fetchData };
