import React from 'react';
import { render, screen, within, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import ComparisonTable from '../../src/components/ComparisonTable';

// Mock data for the table
const mockItems = [
  {
    id: '1',
    cpu: 'Intel i7-10700K',
    gpu: 'NVIDIA RTX 3070',
    ram: '16GB',
    storage: '1TB SSD',
    psu: '650W',
    case: 'NZXT H510',
    price: 1200,
    benchmark: 8500,
    brand: 'BrandA',
  },
  {
    id: '2',
    cpu: 'AMD Ryzen 9 5900X',
    gpu: 'AMD Radeon RX 6800 XT',
    ram: '32GB',
    storage: '2TB SSD',
    psu: '750W',
    case: 'Corsair 4000D',
    price: 1800,
    benchmark: 9500,
    brand: 'BrandB',
  },
];

// Helper to render component within router (for navigation)
function renderComponent(props = {}) {
  return render(
    <BrowserRouter>
      <ComparisonTable items={mockItems} {...props} />
    </BrowserRouter>
  );
}

describe('ComparisonTable UI', () => {
  test('renders all required columns', () => {
    renderComponent();

    const columnHeaders = [
      'CPU',
      'GPU',
      'RAM',
      'Storage',
      'PSU',
      'Case',
      'Price',
      'Benchmark Score',
      'Brand',
    ];

    columnHeaders.forEach((header) => {
      expect(screen.getByRole('columnheader', { name: new RegExp(header, 'i') })).toBeInTheDocument();
    });
  });

  test('displays rows with correct data', () => {
    renderComponent();

    // Verify each mock item appears as a row
    mockItems.forEach((item) => {
      const row = screen.getByTestId(`comparison-row-${item.id}`);
      expect(row).toBeInTheDocument();

      // Check each cell content
      expect(within(row).getByText(item.cpu)).toBeInTheDocument();
      expect(within(row).getByText(item.gpu)).toBeInTheDocument();
      expect(within(row).getByText(item.ram)).toBeInTheDocument();
      expect(within(row).getByText(item.storage)).toBeInTheDocument();
      expect(within(row).getByText(item.psu)).toBeInTheDocument();
      expect(within(row).getByText(item.case)).toBeInTheDocument();
      expect(within(row).getByText(`$${item.price}`)).toBeInTheDocument();
      expect(within(row).getByText(item.benchmark.toString())).toBeInTheDocument();
      expect(within(row).getByText(item.brand)).toBeInTheDocument();
    });
  });

  test('allows sorting by any column', async () => {
    renderComponent();

    // Click the "Price" header to sort ascending
    const priceHeader = screen.getByRole('columnheader', { name: /price/i });
    await userEvent.click(priceHeader);

    const rowsAfterFirstSort = screen.getAllByTestId(/^comparison-row-/);
    const pricesAsc = rowsAfterFirstSort.map((row) => Number(within(row).getByText(/\$\d+/).textContent.replace('$', '')));
    expect(pricesAsc).toEqual([...pricesAsc].sort((a, b) => a - b));

    // Click again to sort descending
    await userEvent.click(priceHeader);
    const rowsAfterSecondSort = screen.getAllByTestId(/^comparison-row-/);
    const pricesDesc = rowsAfterSecondSort.map((row) => Number(within(row).getByText(/\$\d+/).textContent.replace('$', '')));
    expect(pricesDesc).toEqual([...pricesDesc].sort((a, b) => b - a));
  });

  test('filters rows by price range', async () => {
    renderComponent();

    // Assume there are two inputs with labels "Min Price" and "Max Price"
    const minInput = screen.getByLabelText(/min price/i);
    const maxInput = screen.getByLabelText(/max price/i);

    // Set range to only include the first item ($1200)
    await userEvent.clear(minInput);
    await userEvent.type(minInput, '1000');
    await userEvent.clear(maxInput);
    await userEvent.type(maxInput, '1300');

    // Trigger filter (assume component filters on input change)
    fireEvent.blur(minInput);
    fireEvent.blur(maxInput);

    // Expect only the first row to be visible
    expect(screen.getByTestId('comparison-row-1')).toBeVisible();
    expect(screen.queryByTestId('comparison-row-2')).not.toBeInTheDocument();
  });

  test('row click navigates to detailed spec view', async () => {
    // Mock useNavigate from react-router-dom
    const mockNavigate = jest.fn();
    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useNavigate: () => mockNavigate,
    }));

    renderComponent();

    const firstRow = screen.getByTestId('comparison-row-1');
    await userEvent.click(firstRow);

    expect(mockNavigate).toHaveBeenCalledWith('/specs/1');
  });
});