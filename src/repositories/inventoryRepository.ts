import { InventoryItem } from "../models/inventory";

/**
 * In-memory mock repository for inventory items.
 * In production this would interface with a database.
 */
export class InventoryRepository {
  private store: Map<string, InventoryItem> = new Map();

  async findById(id: string): Promise<InventoryItem | null> {
    return this.store.get(id) ?? null;
  }

  async save(item: InventoryItem): Promise<void> {
    this.store.set(item.id, item);
  }
}