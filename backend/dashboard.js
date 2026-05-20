const SecurityStatus = require('./trackers/securityStatus');

class Dashboard {
  constructor() {
    this.securityStatus = new SecurityStatus();
  }

  async update() {
    await this.securityStatus.fetch();
  }

  getSecurityStatus() {
    return this.securityStatus.getStatus();
  }
}

module.exports = Dashboard;