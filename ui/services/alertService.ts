import axios from 'axios';
import { AlertGroup } from '../types/alert';

/**
 * Fetches alert groups from the API and converts raw payload
 * into strongly‑typed objects.
 *
 * @throws {Error} when the request fails or the payload is malformed.
 */
export const fetchAlertGroups = async (): Promise<AlertGroup[]> => {
  try {
    const { data } = await axios.get<{ groups: any[] }>('/api/alert-groups');

    // Defensive mapping – any missing field will cause an explicit error.
    return data.groups.map((g) => {
      if (
        !g.id ||
        !g.title ||
        !g.service ||
        !g.severity ||
        typeof g.alertCount !== 'number' ||
        !g.firstSeen ||
        !g.lastSeen ||
        !Array.isArray(g.memberAlerts)
      ) {
        throw new Error('Malformed alert group payload');
      }

      return {
        id: String(g.id),
        title: String(g.title),
        service: String(g.service),
        severity: g.severity as Severity,
        alertCount: Number(g.alertCount),
        firstSeen: new Date(g.firstSeen),
        lastSeen: new Date(g.lastSeen),
        memberAlerts: g.memberAlerts.map((a: any) => ({
          id: String(a.id),
          message: String(a.message),
          timestamp: new Date(a.timestamp),
        })),
      };
    });
  } catch (err) {
    // Re‑throw with a clearer message for the UI layer.
    const message = axios.isAxiosError(err)
      ? `Alert service unavailable: ${err.message}`
      : (err as Error).message;
    throw new Error(message);
  }
};