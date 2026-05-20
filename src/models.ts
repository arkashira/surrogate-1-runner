export interface Policy {
  id: string;
  limit: number; // The limit for the resource usage
  // Add other policy properties as needed
}

export interface Violation {
  id: string;
  message: string;
  details: object; // Additional details about the violation
}