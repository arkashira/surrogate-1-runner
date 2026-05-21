import crypto from 'crypto';

const getUserData = async () => {
  // Simulate fetching user data from local storage
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        username: 'testUser',
        contributions: [
          { id: 1, amount: 100 },
          { id: 2, amount: 200 },
        ],
      });
    }, 100);
  });
};

const encryptData = (data) => {
  const cipher = crypto.createCipher('aes-256-cbc', 'secret-key');
  let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted;
};

const downloadFile = (content, filename) => {
  const blob = new Blob([content], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

export { getUserData, encryptData, downloadFile };