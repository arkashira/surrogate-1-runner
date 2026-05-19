export interface InventoryItem {
  id: string;
  name: string;
  quantity: number;
  updatedAt: number;          // epoch ms
  // …any other fields you need
}

export interface UpdateEvent {
  type: 'inventory_update';
  payload: InventoryItem;
  updateId: string;           // client‑generated id
  timestamp: number;
}

export interface AckEvent {
  type: 'ack';
  updateId: string;
}

export interface ConflictEvent {
  type: 'conflict';
  localVersion: InventoryItem;
  remoteVersion: InventoryItem;
}

export type ServerEvent =
  | AckEvent
  | UpdateEvent
  | ConflictEvent
  | { type: 'full_sync'; payload: InventoryItem[] };