export interface InventoryItem {
  id: string;
  name: string;
  quantity: number;
  _version: number; // optimistic concurrency token
}