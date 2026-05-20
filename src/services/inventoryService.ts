import { InventoryItem } from "../models/inventory";
import { InventoryRepository } from "../repositories/inventoryRepository";

/**
 * Service layer for inventory operations.
 * Handles optimistic updates, conflict detection, and persistence.
 */
export class InventoryService {
  private repo: InventoryRepository;

  constructor() {
    this.repo = new InventoryRepository();
  }

  /**
   * Updates an inventory item optimistically.
   *
   * @param id The item ID.
   * @param data Partial data to merge into the existing item.
   * @returns The updated item, or an object containing conflict info.
   */
  async updateItem(
    id: string,
    data: Partial<InventoryItem>
  ): Promise<InventoryItem | { conflict: true; remote: InventoryItem }> {
    const current = await this.repo.findById(id);
    if (!current) {
      throw new Error(`Item ${id} not found`);
    }

    // Simple conflict check: if the current version differs from the one
    // the client believes (assumed to be in data._version), we flag a conflict.
    const clientVersion = data._version ?? null;
    if (clientVersion !== null && clientVersion !== current._version) {
      return { conflict: true, remote: current };
    }

    const updated = { ...current, ...data, _version: current._version + 1 };
    await this.repo.save(updated);
    return updated;
  }
}