export interface ClawVariant {
  id: string;
  name: string;
  capabilities: {
    [key: string]: boolean;
  };
}