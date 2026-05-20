import React from 'react';
import { render, screen } from '@testing-library/react';
import Overlay from '../Overlay';

describe('Overlay component', () => {
  it('renders ReactNode children directly without sanitization', () => {
    const mockFn = jest.fn();
    render(
      <Overlay>
        <button onClick={mockFn}>Click Me</button>
      </Overlay>
    );
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('sanitizes string HTML and removes malicious attributes', () => {
    const malicious = '<img src=x onerror=alert(1) />';
    const { container } = render(<Overlay>{malicious}</Overlay>);
    const img = container.querySelector('img');
    
    expect(img).toBeInTheDocument();
    // DOMPurify should strip the onerror handler
    expect(img).not.toHaveAttribute('onerror');
  });

  it('blocks touch events when allowTouch is false (default)', () => {
    render(<Overlay allowTouch={false}>Content</Overlay>);
    const overlay = screen.getByTestId('overlay-container');
    // Corrected: 'auto' blocks clicks from reaching the background
    expect(overlay).toHaveStyle('pointer-events: auto');
  });

  it('allows touch events to pass through when allowTouch is true', () => {
    render(<Overlay allowTouch={true}>Content</Overlay>);
    const overlay = screen.getByTestId('overlay-container');
    // 'none' allows clicks to pass through to elements behind
    expect(overlay).toHaveStyle('pointer-events: none');
  });
});