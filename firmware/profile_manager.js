const fs = require('fs-extra');
const path = require('path');
const crypto = require('crypto');
const cloudStorage = require('./cloud_storage.js'); // Assume cloud storage module exists

const PROFILES_DIR = './profiles';
const VERSIONS_DIR = './versions';
const CLOUD_BACKUP_DIR = 'axentx/profiles';

async function init() {
  await fs.ensureDir(PROFILES_DIR);
  await fs.ensureDir(VERSIONS_DIR);
}

async function saveProfile(profile, version) {
  const profilePath = path.join(PROFILES_DIR, `${version}.json`);
  await fs.writeJson(profilePath, profile);
  await saveVersion(version);
}

async function loadProfile(version) {
  const profilePath = path.join(PROFILES_DIR, `${version}.json`);
  return await fs.readJson(profilePath);
}

async function saveVersion(version) {
  const versionsPath = path.join(VERSIONS_DIR, 'versions.json');
  let versions = await fs.readJson(versionsPath) || [];
  versions.push(version);
  await fs.writeJson(versionsPath, versions);
}

async function getLatestVersion() {
  const versionsPath = path.join(VERSIONS_DIR, 'versions.json');
  let versions = await fs.readJson(versionsPath) || [];
  return versions[versions.length - 1];
}

async function backupToCloud(version) {
  const profilePath = path.join(PROFILES_DIR, `${version}.json`);
  const profile = await fs.readJson(profilePath);
  await cloudStorage.upload(CLOUD_BACKUP_DIR, `${version}.json`, profile);
}

async function restoreFromCloud(version) {
  const profile = await cloudStorage.download(CLOUD_BACKUP_DIR, `${version}.json`);
  await saveProfile(profile, version);
}

async function rollback(version) {
  const latestVersion = await getLatestVersion();
  if (version === latestVersion) {
    throw new Error('Cannot rollback to the latest version');
  }
  await restoreFromCloud(version);
}

module.exports = {
  init,
  saveProfile,
  loadProfile,
  backupToCloud,
  restoreFromCloud,
  rollback,
};