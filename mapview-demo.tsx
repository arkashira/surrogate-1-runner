// Jest + React Testing Library

describe('MapView Component', () => {
  test('renders with default props', () => {
    const { container } = render(<MapView />);
    expect(container.querySelector('.mapview')).toBeInTheDocument();
  });

  test('accepts center and zoom props', () => {
    render(<MapView center={[40.7128, -74.0060]} zoom={12} />);
    expect(screen.getByTestId('mapview')).toHaveAttribute('data-center', '40.7128,-74.0060');
  });

  test('fires onMove callback when position changes', () => {
    const onMove = jest.fn();
    render(<MapView onMove={onMove} />);
    // Simulate position change
    fireEvent.move(screen.getByTestId('mapview'), { center: [40.73, -74.02] });
    expect(onMove).toHaveBeenCalledWith({ center: [40.73, -74.02] };
  });
});

describe('Overlay Component', () => {
  test('renders children content', () => {
    render(<Overlay><span>Marker</span></Overlay>);
    expect(screen.getByText('Marker')).toBeInTheDocument();
  });

  test('accepts position prop', () => {
    render(<Overlay position={[40.7128, -74.0060]} />);
    expect(screen.getByTestId('overlay')).toHaveAttribute('data-position', '40.7128,-74.0060');
  });
});

describe('Demo: mapview-demo.tsx', () => {
  test('initial render shows overlay at starting position', () => {
    render(<MapViewDemo />);
    expect(screen.getByTestId('overlay')).toHaveAttribute('data-position', '40.7128,-74.0060');
  });

  test('overlay position updates after 3 seconds', async () => {
    render(<MapViewDemo />);
    await waitFor(() => {
      expect(screen.getByTestId('overlay')).toHaveAttribute('data-position', '40.73,-74.02');
    }, { timeout: 4000 });
  });
});