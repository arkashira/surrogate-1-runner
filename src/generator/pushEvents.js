#!/usr/bin/env node
// src/generator/pushEvents.js
const http = require('http');
const fs = require('fs');
const path = require('path');

const API_URL = 'http://sandbox:8080/api/v1/events';
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 1000;

function readEventsFromInput() {
  let rawData = '';
  process.stdin.setEncoding('utf8');

  return new Promise((resolve, reject) => {
    process.stdin.on('data', (chunk) => {
      rawData += chunk;
    });

    process.stdin.on('end', () => {
      try {
        const events = JSON.parse(rawData);
        if (!Array.isArray(events)) {
          throw new Error('Input must be a JSON array of events');
        }
        resolve(events);
      } catch (err) {
        reject(new Error(`Failed to parse input JSON: ${err.message}`));
      }
    });

    process.stdin.on('error', reject);
  });
}

async function postEvents(events) {
  const postData = JSON.stringify(events);
  const options = {
    hostname: 'sandbox',
    port: 8080,
    path: '/api/v1/events',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ statusCode: res.statusCode, body });
        } else {
          reject(new Error(`Server responded with status ${res.statusCode}: ${body}`));
        }
      });
    });

    req.on('error', (err) => {
      reject(new Error(`Failed to connect to sandbox: ${err.message}`));
    });

    req.write(postData);
    req.end();
  });
}

async function pushEventsWithRetry(events, attempt = 1) {
  try {
    const result = await postEvents(events);
    console.log(`Successfully posted ${events.length} events (attempt ${attempt})`);
    return { success: true, count: events.length };
  } catch (err) {
    if (attempt >= MAX_RETRIES) {
      throw new Error(`Failed to push events after ${MAX_RETRIES} attempts: ${err.message}`);
    }
    console.error(`Attempt ${attempt} failed: ${err.message}`);
    await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY_MS * attempt));
    return pushEventsWithRetry(events, attempt + 1);
  }
}

async function main() {
  try {
    const events = await readEventsFromInput();
    console.log(`Received ${events.length} events to push`);

    const result = await pushEventsWithRetry(events);

    if (result.success) {
      console.log(`✓ Pushed ${result.count} events to sandbox`);
      process.exit(0);
    }
  } catch (err) {
    console.error(`✗ Error: ${err.message}`);
    process.exit(1);
  }
}

main();