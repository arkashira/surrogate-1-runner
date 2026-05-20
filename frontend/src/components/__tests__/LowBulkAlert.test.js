import React from 'react';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import LowBulkAlert from '../LowBulkAlert';

// Mock localStorage using Object.defineProperty for better JSDOM compatibility
const localStorageMock = (() => {
  let store = {};
  return {
    getItem(key) {
      return store[key] || null;
    },
    setItem(key, value) {
      store[key] = value.toString();
    },
    removeItem(key) {
      delete store[key];
    },
    clear() {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

afterEach(() => {
  cleanup();
  localStorage.clear();
});

describe('LowBulkAlert visibility thresholds', () => {
  // Helper to render component with a specific remaining percentage
  const renderAlert = (remainingPercent) => {
    render(
      <LowBulkAlert
        totalBulk={100}
        remainingBulk={remainingPercent}
        purchaseUrl="https://placeholder.purchase.url"
      />
    );
  };

  test('does not show alert when remaining > 15%', () => {
    renderAlert(16);
    expect(screen.queryByRole('banner')).not.toBeInTheDocument();
  });

  test('shows alert when remaining exactly 15%', () => {
    renderAlert(15);
    const banner = screen.getByRole('banner');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveTextContent(/low bulk credit/i);
    
    // Verify the CTA is actionable
    const cta = screen.getByRole('link', { name: /purchase bulk credits/i });
    expect(cta).toHaveAttribute('href', expect.stringContaining('placeholder'));
  });

  test('shows alert when remaining < 15% (e.g., 14.9%)', () => {
    renderAlert(14.9);
    expect(screen.getByRole('banner')).toBeInTheDocument();
  });

  test('dismiss button hides alert and persists dismissal in localStorage', () => {
    renderAlert(14);
    const dismissBtn = screen.getByRole('button', { name: /dismiss/i });
    
    fireEvent.click(dismissBtn);
    
    // UI should update immediately
    expect(screen.queryByRole('banner')).not.toBeInTheDocument();
    
    // State should be persisted
    expect(localStorage.getItem('lowBulkAlertDismissed')).toBe('true');
  });

  test('alert remains hidden on reload if dismissal is persisted and condition still applies', () => {
    // 1. Initial render with low bulk
    renderAlert(14);
    expect(screen.getByRole('banner')).toBeInTheDocument();

    // 2. Dismiss the alert
    fireEvent.click(screen.getByRole('button', { name: /dismiss/i }));
    expect(screen.queryByRole('banner')).not.toBeInTheDocument();

    // 3. Simulate reload (re-render component) while condition still applies
    cleanup();
    renderAlert(14);
    
    // Alert should stay hidden because user previously dismissed it
    expect(screen.queryByRole('banner')).not.toBeInTheDocument();
  });

  test('alert reappears if condition clears (purchase) and returns (low again)', () => {
    // 1. User is low, dismisses alert
    renderAlert(14);
    fireEvent.click(screen.getByRole('button', { name: /dismiss/i }));
    expect(screen.queryByRole('banner')).not.toBeInTheDocument();

    // 2. User purchases credits (condition clears)
    renderAlert(20); 
    expect(screen.queryByRole('banner')).not.toBeInTheDocument();

    // 3. User runs low again
    renderAlert(14);
    
    // Alert MUST reappear. The previous dismissal was for a previous "session".
    expect(screen.getByRole('banner')).toBeInTheDocument();
  });
});