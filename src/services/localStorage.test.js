const LocalStorage = require('./localStorage');
const fs = require('fs');
const path = require('path');

describe('LocalStorage', () => {
  let localStorage;

  beforeEach(async () => {
    localStorage = new LocalStorage();
    await localStorage.init();
  });

  afterEach(async () => {
    await fs.promises.unlink(localStorage.storagePath);
  });

  it('should save and retrieve data', async () => {
    const data = { foo: 'bar' };
    await localStorage.saveData(data);
    const retrievedData = await localStorage.getData();
    expect(retrievedData).toEqual(data);
  });

  it('should export data', async () => {
    const data = { foo: 'bar' };
    await localStorage.saveData(data);
    const exportedData = await localStorage.exportData();
    expect(exportedData).toBe(JSON.stringify(data, null, 2));
  });

  it('should encrypt and decrypt data', async () => {
    const data = 'Hello, World!';
    const encryptedData = localStorage.encrypt(data);
    const decryptedData = localStorage.decrypt(encryptedData);
    expect(decryptedData).toBe(data);
  });
});