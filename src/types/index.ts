export interface Dashboard {
  id: number;
  name: string;
}

export interface Alert {
  id: number;
  name: string;
}

/** Description of a pricing tier */
export interface TierFeatures {
  /** Human readable name */
  name: string;
  /** Number of dashboards – `unlimited` or a concrete count */
  dashboards: number | 'unlimited';
  /** Number of alerts – `-1` means unlimited */
  alerts: number;
  /** Is API access included? */
  apiAccess: boolean;
  /** Is the web UI included? */
  webInterface: boolean;
}