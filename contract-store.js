const fs = require('fs');
const path = require('path');

class ContractStore {
  constructor(contractsDir) {
    this.contractsDir = contractsDir;
  }

  storeSignature(signature) {
    // Marshal the signature to JSON
    const signatureJSON = JSON.stringify(signature);

    // Store the signature in the contracts directory
    const contractFile = path.join(this.contractsDir, `contract-${Date.now()}.json`);
    fs.writeFileSync(contractFile, signatureJSON);
  }

  compareSignatures(baselineSignature, liveSignature) {
    // Compare the baseline signature with the live signature
    // Return true if the signatures match within 50ms, false otherwise
    const durationDiff = Math.abs(baselineSignature.duration - liveSignature.duration);
    return durationDiff <= 50;
  }
}

module.exports = ContractStore;