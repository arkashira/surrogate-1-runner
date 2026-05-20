import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing';
import { GET_ORGANIZATION_BILLING } from '../utils/queries';
import Billing from '../Billing';

const mocks = [
  {
    request: {
      query: GET_ORGANIZATION_BILLING,
    },
    result: {
      data: {
        organization: {
          id: 'org-id',
          billing: {
            surrogateShellMinutes: 10,
            surrogateShellCost: 1.99,
          },
        },
      },
    },
  },
];

describe('Billing component', () => {
  it('renders correctly', () => {
    const { getByText } = render(
      <MockedProvider mocks={mocks}>
        <Billing />
      </MockedProvider>
    );

    expect(getByText('Surrogate Shell Usage')).toBeInTheDocument();
    expect(getByText('10 minutes')).toBeInTheDocument();
    expect(getByText('$1.99')).toBeInTheDocument();
  });
});