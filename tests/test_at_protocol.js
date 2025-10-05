const { handleAccount } = require('../backend/at_protocol');

test('AT Protocol account creation and wallet linking', async () => {
  const user = { username: 'testuser' };
  const wallet = '0x123';
  const result = await handleAccount(user, wallet);
  expect(result.account).toBeDefined();
  expect(result.linked).toBeTruthy();
});
