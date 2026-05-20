import axios from 'axios';

export const api = axios.create({
  baseURL: 'https://api.axentx.com',
  timeout: 10_000,
});