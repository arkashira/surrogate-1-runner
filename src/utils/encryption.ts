import CryptoJS from 'crypto-js';

const SALT = 'your-salt-here';
const ITERATIONS = 10000;

export const encryptData = async (passcode, data) => {
  const key = CryptoJS.PBKDF2(passcode, SALT, { keySize: 256/32, iterations: ITERATIONS });
  const encrypted = CryptoJS.AES.encrypt(JSON.stringify(data), key.toString(), { mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
  return encrypted.toString();
};

export const decryptData = async (passcode, encryptedData) => {
  const key = CryptoJS.PBKDF2(passcode, SALT, { keySize: 256/32, iterations: ITERATIONS });
  const decrypted = CryptoJS.AES.decrypt(encryptedData, key.toString(), { mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
  return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
};

export const wipeData = () => {
  // Implement data wiping logic here
  console.log('Data wiped');
};