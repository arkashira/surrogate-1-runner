// Panel.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Panel from './Panel';
import * as api from '../api/surrogate'; // mockable module

jest.mock('../api/surrogate');

describe('Panel component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders header and input area', () => {
    render(<Panel />);
    expect(screen.getByText(/AI Assistant/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Type a message.../i)).toBeInTheDocument();
  });

  test('sends message and displays response', async () => {
    const mockResponse = { id: 'msg1', text: 'Hello from backend' };
    (api.sendMessage as jest.Mock).mockResolvedValue(mockResponse);

    render(<Panel />);
    const input = screen.getByPlaceholderText(/Type a message.../i);
    fireEvent.change(input, { target: { value: 'Hi' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });

    await waitFor(() => expect(api.sendMessage).toHaveBeenCalledWith('Hi'));
    expect(screen.getByText(/Hello from backend/i)).toBeInTheDocument();
  });

  test('shows error banner on request failure', async () => {
    (api.sendMessage as jest.Mock).mockRejectedValue(new Error('Network error'));

    render(<Panel />);
    const input = screen.getByPlaceholderText(/Type a message.../i);
    fireEvent.change(input, { target: { value: 'Hi' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/Network error/i));
  });

  test('aborts request on unmount', async () => {
    const abortSpy = jest.fn();
    const abortControllerMock = { abort: abortSpy, signal: {} as AbortSignal };
    jest.spyOn(window, 'AbortController').mockReturnValue(abortControllerMock as any);

    const { unmount } = render(<Panel />);
    const input = screen.getByPlaceholderText(/Type a message.../i);
    fireEvent.change(input, { target: { value: 'Hi' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });

    unmount();
    expect(abortSpy).toHaveBeenCalled();
  });
});