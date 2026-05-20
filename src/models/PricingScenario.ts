export interface Tier {
  name: string;
  price: number;          // monthly price in USD
  features?: string[];
  conversionRate: number; // 0‑1 probability that a user upgrades to this tier
  monthlyChurnRate: number; // 0‑1 probability that a user leaves this tier each month
}

export interface PricingScenarioJSON {
  id: string;
  name: string;
  tiers: Tier[];
  baseUsers: number;
  growthRate: number;      // e.g. 0.05 = 5 % monthly growth
  projectionMonths: number;
  createdAt: string;       // ISO string
}

export class PricingScenario {
  public readonly id: string;
  public readonly name: string;
  public readonly tiers: Tier[];
  public readonly baseUsers: number;
  public readonly growthRate: number;
  public readonly projectionMonths: number;
  public readonly createdAt: Date;

  constructor({
    id,
    name,
    tiers = [],
    baseUsers = 0,
    growthRate = 0,
    projectionMonths = 12,
    createdAt,
  }: Partial<PricingScenarioJSON> & { name: string }) {
    this.id = id ?? PricingScenario.generateId();
    this.name = name;
    this.tiers = tiers.map(t => PricingScenario.validateTier(t));
    this.baseUsers = baseUsers;
    this.growthRate = growthRate;
    this.projectionMonths = projectionMonths;
    this.createdAt = createdAt ? new Date(createdAt) : new Date();
  }

  /* ------------------------------------------------------------------ */
  /*  Helpers                                                          */
  /* ------------------------------------------------------------------ */
  static generateId(): string {
    return `scenario_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
  }

  static validateTier(tier: Tier): Tier {
    if (!tier.name) throw new Error('Tier must have a name');
    if (typeof tier.price !== 'number' || tier.price < 0)
      throw new Error('Tier price must be a non‑negative number');
    if (tier.conversionRate < 0 || tier.conversionRate > 1)
      throw new Error('conversionRate must be between 0 and 1');
    if (tier.monthlyChurnRate < 0 || tier.monthlyChurnRate > 1)
      throw new Error('monthlyChurnRate must be between 0 and 1');
    return {
      ...tier,
      features: tier.features ?? [],
      conversionRate: tier.conversionRate ?? 0.1,
      monthlyChurnRate: tier.monthlyChurnRate ?? 0.05,
    };
  }

  /* ------------------------------------------------------------------ */
  /*  Persistence                                                      */
  /* ------------------------------------------------------------------ */
  toJSON(): PricingScenarioJSON {
    return {
      id: this.id,
      name: this.name,
      tiers: this.tiers,
      baseUsers: this.baseUsers,
      growthRate: this.growthRate,
      projectionMonths: this.projectionMonths,
      createdAt: this.createdAt.toISOString(),
    };
  }

  static fromJSON(json: PricingScenarioJSON): PricingScenario {
    return new PricingScenario(json);
  }
}