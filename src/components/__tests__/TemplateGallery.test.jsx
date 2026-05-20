import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TemplateGallery from '../TemplateGallery';
import { useTemplates } from '../hooks/useTemplates';

jest.mock('../hooks/useTemplates');

describe('TemplateGallery', () => {
  const mockTemplates = [
    { id: 1, name: 'Blog outline generator', description: 'Generate a blog outline' },
    { id: 2, name: 'Social media scheduler', description: 'Schedule social media posts' },
  ];

  beforeEach(() => {
    useTemplates.mockReturnValue({
      templates: mockTemplates,
      error: null,
      isLoading: false,
    });
  });

  it('renders template gallery with templates', () => {
    render(<TemplateGallery />);
    expect(screen.getByText('Template Gallery')).toBeInTheDocument();
    mockTemplates.forEach(template => {
      expect(screen.getByText(template.name)).toBeInTheDocument();
      expect(screen.getByText(template.description)).toBeInTheDocument();
    });
  });

  it('renders loading state when loading', () => {
    useTemplates.mockReturnValueOnce({
      templates: [],
      error: null,
      isLoading: true,
    });
    render(<TemplateGallery />);
    expect(screen.getByText('Loading templates...')).toBeInTheDocument();
  });

  it('renders error state when error occurs', () => {
    const error = new Error('Failed to fetch templates');
    useTemplates.mockReturnValueOnce({
      templates: [],
      error,
      isLoading: false,
    });
    render(<TemplateGallery />);
    expect(screen.getByText(`Error: ${error.message}`)).toBeInTheDocument();
  });

  it('renders empty state when no templates available', () => {
    useTemplates.mockReturnValueOnce({
      templates: [],
      error: null,
      isLoading: false,
    });
    render(<TemplateGallery />);
    expect(screen.getByText('No templates available')).toBeInTheDocument();
  });

  it('calls handleTemplateSelection when customize button is clicked', () => {
    const handleTemplateSelection = jest.fn();
    // Mock the actual implementation
    jest.spyOn(React, 'useState').mockImplementationOnce((initialState) => [
      initialState,
      jest.fn(),
    ]);
    render(<TemplateGallery />);
    const buttons = screen.getAllByRole('button', { name: 'Customize Template' });
    userEvent.click(buttons[0]);
    expect(handleTemplateSelection).toHaveBeenCalledWith(mockTemplates[0]);
  });
});