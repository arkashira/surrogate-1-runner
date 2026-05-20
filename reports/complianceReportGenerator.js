const fs = require('fs');
const path = require('path');
const { generateReport } = require('./reportGenerator');

class ComplianceReportGenerator {
  constructor(config) {
    this.config = config;
  }

  generateReport() {
    const reportData = generateReport(this.config);
    const reportPath = path.join(__dirname, 'reports', `compliance_${new Date().toISOString()}.json`);
    fs.writeFileSync(reportPath, JSON.stringify(reportData, null, 2));
    console.log(`Compliance report generated and saved to ${reportPath}`);
  }
}

module.exports = ComplianceReportGenerator;