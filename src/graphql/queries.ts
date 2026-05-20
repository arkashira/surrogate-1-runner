import { gql } from '@apollo/client';

export const GET_COST_ANOMALIES = gql`
  query GetCostAnomalies($filters: CostAnomalyFilter) {
    costAnomalies(filters: $filters) {
      id
      severity
      type
      timestamp
      description
      remediation
    }
  }
`;