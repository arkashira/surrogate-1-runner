import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import InvestorReportButton from './InvestorReportButton';

describe('InvestorReportButton', () => {
  it('renders button with correct text', () => {
    const { getByText } = render(<InvestorReportButton />);
    expect(getByText('Generate Investor Report')).toBeInTheDocument();
  });

  it('calls generateInvestorReport when button is clicked', async () => {
    const generateInvestorReportMock = jest.fn();
    const { getByText } = render(
      <InvestorReportButton generateInvestorReport={generateInvestorReportMock} />
    );
    fireEvent.click(getByText('Generate Investor Report'));
    expect(generateInvestorReportMock).toHaveBeenCalledTimes(1);
  });
});