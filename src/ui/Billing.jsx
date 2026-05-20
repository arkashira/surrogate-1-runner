import React from 'react';
import { useQuery, gql } from '@apollo/client';

const GET_ORGANIZATION_BILLING = gql`
  query GetOrganizationBilling {
    organization {
      id
      billing {
        surrogateShellMinutes
        surrogateShellCost
      }
    }
  }
`;

const Billing = () => {
  const { data, loading, error } = useQuery(GET_ORGANIZATION_BILLING);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  const { surrogateShellMinutes, surrogateShellCost } = data.organization.billing;

  const displayMinutes = Math.ceil(surrogateShellMinutes);
  const displayCost = surrogateShellCost.toFixed(2);

  return (
    <div>
      <h2>Surrogate Shell Usage</h2>
      <p>
        {displayMinutes} minutes
      </p>
      <p>
        ${displayCost}
      </p>
    </div>
  );
};

export default Billing;