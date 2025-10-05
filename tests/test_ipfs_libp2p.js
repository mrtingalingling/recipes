const { storeData, fetchData } = require('../backend/ipfs_libp2p');

test('IPFS store and fetch data', async () => {
  const obj = { foo: 'bar' };
  const cid = await storeData(obj);
  expect(cid).toBeDefined();
  const data = await fetchData(cid);
  expect(data).toEqual(obj);
});
