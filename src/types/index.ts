export interface Alert {
  id: string;
  message: string;
  link: string;
  timestamp: string; // ISO string for JSON serialisation
}

export interface Approval {
  id: string;
  message: string;
  link: string;
  timestamp: string;
}