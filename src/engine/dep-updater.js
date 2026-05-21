const fs = require('fs');
const path = require('path');

class DepUpdater {
  constructor(packageJsonPath) {
    this.packageJsonPath = packageJsonPath;
    this.packageJson = null;
    this.dryRun = false;
  }

  setDryRun(enabled) {
    this.dryRun = enabled;
  }

  loadPackageJson() {
    if (!fs.existsSync(this.packageJsonPath)) {
      throw new Error(`Package.json not found at ${this.packageJsonPath}`);
    }

    const content = fs.readFileSync(this.packageJsonPath, 'utf8');
    this.packageJson = JSON.parse(content);
    return this.packageJson;
  }

  savePackageJson() {
    if (this.dryRun) {
      console.log(`[DRY-RUN] Would save package.json to ${this.packageJsonPath}`);
      return;
    }

    // Preserve formatting by using the original indentation
    const originalContent = fs.readFileSync(this.packageJsonPath, 'utf8');
    const indentMatch = originalContent.match(/^\s+/m);
    const indent = indentMatch ? indentMatch[0] : '  ';

    const formattedContent = JSON.stringify(this.packageJson, null, indent);
    fs.writeFileSync(this.packageJsonPath, formattedContent + '\n');
  }

  addDependency(packageName, version) {
    if (!this.packageJson.dependencies) {
      this.packageJson.dependencies = {};
    }

    const existing = this.packageJson.dependencies[packageName];
    if (existing) {
      if (existing === version) {
        console.log(`[INFO] Dependency ${packageName} already at version ${version}`);
        return false;
      }

      // Version conflict: warn and skip
      console.warn(`[CONFLICT] ${packageName} already exists at ${existing}, requested ${version}`);
      return false;
    }

    this.packageJson.dependencies[packageName] = version;
    console.log(`[ADD] Added ${packageName}@${version}`);
    return true;
  }

  updateDependency(packageName, version) {
    if (!this.packageJson.dependencies) {
      this.packageJson.dependencies = {};
    }

    if (!this.packageJson.dependencies[packageName]) {
      console.warn(`[WARN] ${packageName} not found in dependencies`);
      return false;
    }

    const oldVersion = this.packageJson.dependencies[packageName];
    this.packageJson.dependencies[packageName] = version;
    console.log(`[UPDATE] ${packageName}: ${oldVersion} -> ${version}`);
    return true;
  }

  removeDependency(packageName) {
    if (!this.packageJson.dependencies) {
      console.warn(`[WARN] No dependencies section found`);
      return false;
    }

    if (!this.packageJson.dependencies[packageName]) {
      console.warn(`[WARN] ${packageName} not found in dependencies`);
      return false;
    }

    delete this.packageJson.dependencies[packageName];
    console.log(`[REMOVE] Removed ${packageName}`);
    return true;
  }

  getChanges() {
    const changes = {
      added: [],
      updated: [],
      removed: [],
      conflicts: []
    };

    // This would be populated by comparing with a target state
    // For now, return empty changes
    return changes;
  }

  applyChanges(changes) {
    let modified = false;

    for (const [packageName, version] of Object.entries(changes.added)) {
      if (this.addDependency(packageName, version)) {
        modified = true;
      }
    }

    for (const [packageName, version] of Object.entries(changes.updated)) {
      if (this.updateDependency(packageName, version)) {
        modified = true;
      }
    }

    for (const packageName of changes.removed) {
      if (this.removeDependency(packageName)) {
        modified = true;
      }
    }

    if (modified) {
      this.savePackageJson();
    }

    return modified;
  }

  async run() {
    try {
      this.loadPackageJson();
      const changes = this.getChanges();
      const modified = this.applyChanges(changes);

      if (this.dryRun) {
        console.log('\n[DRY-RUN SUMMARY]');
        console.log(`  Added: ${changes.added.length}`);
        console.log(`  Updated: ${changes.updated.length}`);
        console.log(`  Removed: ${changes.removed.length}`);
        console.log(`  Conflicts: ${changes.conflicts.length}`);
      } else {
        console.log('\nChanges applied successfully');
      }

      return modified;
    } catch (error) {
      console.error(`Error: ${error.message}`);
      throw error;
    }
  }
}

// CLI interface
function main() {
  const args = process.argv.slice(2);
  const packageJsonPath = args[0] || 'package.json';
  const dryRun = args.includes('--dry-run');

  const updater = new DepUpdater(packageJsonPath);
  updater.setDryRun(dryRun);

  console.log(`DepUpdater: ${packageJsonPath} (dry-run: ${dryRun})`);

  // In production, this would be called with actual changes from verified imports
  // For now, demonstrate the interface
  updater.run().then(() => {
    process.exit(0);
  }).catch((error) => {
    console.error(error);
    process.exit(1);
  });
}

if (require.main === module) {
  main();
}

module.exports = { DepUpdater };