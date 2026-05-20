import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import VariantList from '../VariantList';

describe('VariantList Component', () => {
  const variants = [
    { name: 'Variant A', description: 'Description A' },
    { name: 'Variant B', description: 'Description B' },
    { name: 'Variant C', description: 'Description C' },
    { name: 'Variant D', description: 'Description D' },
    { name: 'Variant E', description: 'Description E' },
  ];

  it('renders the list of variants', () => {
    render(<VariantList variants={variants} />);
    variants.forEach((variant) => {
      expect(screen.getByText(new RegExp(variant.name))).toBeInTheDocument();
      expect(screen.getByText(new RegExp(variant.description))).toBeInTheDocument();
    });
  });

  it('filters variants by search term', () => {
    render(<VariantList variants={variants} />);
    fireEvent.change(screen.getByPlaceholderText(/search by name or description/i), { target: { value: 'Variant A' } });
    expect(screen.getByText(/Variant A/i)).toBeInTheDocument();
    expect(screen.queryByText(/Variant B/i)).not.toBeInTheDocument();
  });

  it('sorts variants by name', () => {
    render(<VariantList variants={variants} />);
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'name' } });
    const names = screen.getAllByRole('listitem').map((item) => item.querySelector('strong').textContent);
    expect(names).toEqual(['Variant A', 'Variant B', 'Variant C', 'Variant D', 'Variant E']);
  });

  it('sorts variants by description', () => {
    render(<VariantList variants={variants} />);
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'description' } });
    const descriptions = screen.getAllByRole('listitem').map((item) => item.textContent.replace(item.querySelector('strong').textContent, '').trim());
    expect(descriptions).toEqual(['Description A', 'Description B', 'Description C', 'Description D', 'Description E']);
  });
});