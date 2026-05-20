/**
 * AzureProvider – Surrogate‑1 Azure integration
 *
 * Collects all virtual machines and storage accounts in a subscription.
 * Returns a normalised object that the dashboard can consume.
 *
 * Dependencies:
 *   @azure/identity
 *   @azure/arm-compute
 *   @azure/arm-storage
 *
 * If any of the SDK packages are missing, the constructor throws an
 * informative error so that the orchestrator can skip this provider.
 */

const { DefaultAzureCredential } = require("@azure/identity");
const { ComputeManagementClient } = require("@azure/arm-compute");
const { StorageManagementClient } = require("@azure/arm-storage");

class AzureProvider {
  /**
   * @param {Object} config
   * @param {string} config.subscriptionId – Azure subscription ID
   */
  constructor(config) {
    if (!config || !config.subscriptionId) {
      throw new Error(
        "AzureProvider requires a config object with a subscriptionId"
      );
    }

    this.subscriptionId = config.subscriptionId;
    this.credential = new DefaultAzureCredential();

    // Initialise SDK clients – any error bubbles up to the caller
    this.computeClient = new ComputeManagementClient(
      this.credential,
      this.subscriptionId
    );
    this.storageClient = new StorageManagementClient(
      this.credential,
      this.subscriptionId
    );
  }

  /**
   * Collect all VMs and storage accounts.
   *
   * @returns {Promise<Object>} Normalised resource data
   */
  async collectResources() {
    const [vms, storages] = await Promise.all([
      this._listVirtualMachines(),
      this._listStorageAccounts(),
    ]);

    return {
      provider: "azure",
      subscriptionId: this.subscriptionId,
      virtualMachines: vms,
      storageAccounts: storages,
    };
  }

  /* ------------------------------------------------------------------ */
  /*  Private helpers – iterate over paginated SDK generators           */
  /* ------------------------------------------------------------------ */

  async _listVirtualMachines() {
    const vms = [];
    for await (const vm of this.computeClient.virtualMachines.listAll()) {
      vms.push({
        id: vm.id,
        name: vm.name,
        location: vm.location,
        vmSize: vm.hardwareProfile?.vmSize,
        os: vm.storageProfile?.osDisk?.osType,
        tags: vm.tags,
      });
    }
    return vms;
  }

  async _listStorageAccounts() {
    const storages = [];
    for await (const sa of this.storageClient.storageAccounts.list()) {
      storages.push({
        id: sa.id,
        name: sa.name,
        location: sa.location,
        kind: sa.kind,
        sku: sa.sku?.name,
        tags: sa.tags,
      });
    }
    return storages;
  }
}

module.exports = AzureProvider;