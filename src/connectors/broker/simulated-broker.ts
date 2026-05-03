import { Connector, ConnectorError, HealthResult } from '../base-connector';

export interface Order {
  id?: string;
  symbol: string;
  side: 'buy' | 'sell';
  quantity: number;
  price?: number;
  type?: 'market' | 'limit' | 'stop';
}

export interface PlaceOrderResult {
  order_id: string;
  status: 'placed' | 'rejected';
  symbol: string;
  filled_quantity: number;
  remaining_quantity: number;
  avg_price?: number;
}

export interface CancelOrderResult {
  order_id: string;
  status: 'cancelled' | 'not_found' | 'already_filled';
}

export class SimulatedBroker implements Connector {
  private connected = false;
  private orders = new Map<string, Order & { id: string; status: 'open' | 'filled' | 'cancelled' }>();
  private orderCounter = 0;

  async connect(): Promise<void> {
    await new Promise((resolve) => setTimeout(resolve, 10));
    this.connected = true;
  }

  async call<T = unknown>(method: string, params: Record<string, unknown> = {}): Promise<T> {
    if (!this.connected) {
      throw new ConnectorError('NOT_CONNECTED', 'Broker is not connected');
    }

    switch (method) {
      case 'place_order':
        return this.placeOrder(params as { order: Order }) as Promise<T>;
      case 'cancel_order':
        return this.cancelOrder(params as { order_id: string }) as Promise<T>;
      default:
        throw new ConnectorError('METHOD_NOT_FOUND', `Method ${method} not supported`);
    }
  }

  async health(): Promise<HealthResult> {
    const start = Date.now();
    await new Promise((resolve) => setTimeout(resolve, 1));
    const latency = Date.now() - start;

    return {
      status: this.connected ? 'healthy' : 'unhealthy',
      latency_ms: latency,
      details: {
        orders_count: this.orders.size,
        type: 'simulated',
      },
      timestamp: new Date().toISOString(),
    };
  }

  async placeOrder(params: { order: Order }): Promise<PlaceOrderResult> {
    const order = params.order;
    const id = `sim_${++this.orderCounter}`;
    const storedOrder = { ...order, id, status: 'open' as const };
    this.orders.set(id, storedOrder);

    // Simulate full fills for market orders; otherwise remain open
    let filled = 0;
    if (order.type === 'market') {
      filled = order.quantity;
      storedOrder.status = 'filled';
    }

    return {
      order_id: id,
      status: 'placed',
      symbol: order.symbol,
      filled_quantity: filled,
      remaining_quantity: order.quantity - filled,
      avg_price: order.price,
    };
  }

  async cancelOrder(params: { order_id: string }): Promise<CancelOrderResult> {
    const order = this.orders.get(params.order_id);
    if (!order) {
      return { order_id: params.order_id, status: 'not_found' };
    }
    if (order.status === 'filled') {
      return { order_id: params.order_id, status: 'already_filled' };
    }
    order.status = 'cancelled';
    return { order_id: params.order_id, status: 'cancelled' };
  }
}