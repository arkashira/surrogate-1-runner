export const GET_ORGANIZATION_BILLING = `
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