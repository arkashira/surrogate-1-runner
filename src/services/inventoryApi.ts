export interface InventoryItem {
  id: number;
  product: string;
  location: string;
  status: string;
}

export async function fetchInventory(): Promise<InventoryItem[]> {
  const res = await fetch('/api/inventory');
  if (!res.ok) throw new Error('Network response was not ok');
  return res.json();
}