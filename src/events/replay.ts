/**
 * Replay utility for execution event logs.
 *
 * Requirements:
 * - Read event log entries, reconstruct a pipeline run, emit per-run summary JSON.
 * - Support successful executions (with fills) and failed executions (with error codes).
 * - Output must be deterministic and machine-readable (JSON) for reconciliation/compliance.
 */

export type OrderSide = 'buy' | 'sell';
export type OrderType = 'market' | 'limit' | 'stop' | 'stop_limit';

export interface Order {
  id: string;
  symbol: string;
  side: OrderSide;
  type: OrderType;
  qty: number;
  price?: number;
  timestamp: string; // ISO 8601
}

export interface Fill {
  orderId: string;
  fillPrice: number;
  fillQty: number;
  timestamp: string; // ISO 8601
}

export interface ExecutionSuccess {
  event: 'execution_success';
  order: Order;
  fill: Fill;
}

export interface ExecutionFailed {
  event: 'execution_failed';
  order: Order;
  errorCode: string;
  errorMessage?: string;
  timestamp: string; // ISO 8601
}

export type EventLogEntry = ExecutionSuccess | ExecutionFailed;

function isoTime(value: unknown): string | null {
  if (typeof value !== 'string') return null;
  const n = Date.parse(value);
  return Number.isNaN(n) ? null : new Date(n).toISOString();
}

function compareIso(a: string | null, b: string | null): number {
  if (a === null && b === null) return 0;
  if (a === null) return 1;
  if (b === null) return -1;
  return a < b ? -1 : a > b ? 1 : 0;
}

export interface RunSummary {
  runId: string;
  generatedAt: string;
  eventCount: number;
  successCount: number;
  failureCount: number;
  symbols: string[];
  fills: Array<{
    orderId: string;
    symbol: string;
    side: OrderSide;
    fillPrice: number;
    fillQty: number;
    timestamp: string;
    notional: number;
  }>;
  errors: Array<{
    orderId: string;
    symbol: string;
    errorCode: string;
    errorMessage?: string;
    timestamp: string;
  }>;
  totals: {
    totalFilledQty: number;
    totalNotional: number;
    avgFillPrice: number | null;
  };
  time: {
    firstEventAt: string | null;
    lastEventAt: string | null;
    durationMs: number | null;
  };
}

export class ReplayEngine {
  private events: EventLogEntry[] = [];
  private fills: Array<{
    orderId: string;
    symbol: string;
    side: OrderSide;
    fillPrice: number;
    fillQty: number;
    timestamp: string;
  }> = [];
  private errors: Array<{
    orderId: string;
    symbol: string;
    errorCode: string;
    errorMessage?: string;
    timestamp: string;
  }> = [];
  private symbolsSet = new Set<string>();

  /**
   * Load events (expected in chronological order).
   * If ordering cannot be guaranteed, caller should sort by timestamp before load.
   */
  load(events: EventLogEntry[]): this {
    this.events = events.slice(); // defensive shallow copy
    return this;
  }

  /**
   * Replay loaded events and compute run state.
   */
  reconstruct(): this {
    this.fills = [];
    this.errors = [];
    this.symbolsSet.clear();

    for (const ev of this.events) {
      const { order } = ev;
      const symbol = order?.symbol;
      if (symbol) this.symbolsSet.add(symbol);

      if (ev.event === 'execution_success') {
        const ts = isoTim
