/**
 * Integration tests for the resolver module.
 *
 * They verify that the public `resolve` API correctly delegates to the
 * strategy‑specific implementations for:
 *   1️⃣ AX direct attempt
 *   2️⃣ CGEvent Cmd+V attempt
 *   3️⃣ AppleScript attempt
 *
 * All external side‑effects are mocked so the suite runs in a pure Node
 * environment (no UI, no AppleScript interpreter needed).
 */

const resolver = require('./resolver');          // <-- the module under test
const utils    = require('./utils');             // shared payload builders

// ---------------------------------------------------------------------------
// Global Jest setup for each test – ensures a clean mock slate
// ---------------------------------------------------------------------------
beforeEach(() => {
  jest.resetAllMocks();
  jest.restoreAllMocks();
});

// ---------------------------------------------------------------------------
// 1️⃣ AX Direct Attempt
// ---------------------------------------------------------------------------
describe('Resolver – AX Direct Attempt', () => {
  test('resolves successfully when AX payload is valid', async () => {
    const payload = utils.buildAxDirectPayload('https://example.com');

    // Mock the low‑level implementation that talks to the AX API
    jest.spyOn(resolver, 'handleAxDirect')
        .mockResolvedValue({ success: true, data: 'ok' });

    const result = await resolver.resolve({ type: 'ax-direct', payload });

    expect(resolver.handleAxDirect).toHaveBeenCalledWith(payload);
    expect(result).toEqual({ success: true, data: 'ok' });
  });
});

// ---------------------------------------------------------------------------
// 2️⃣ CGEvent Cmd+V Attempt
// ---------------------------------------------------------------------------
describe('Resolver – CGEvent Cmd+V Attempt', () => {
  test('processes a Cmd+V CGEvent and returns true', async () => {
    const payload = utils.buildCgEventPayload('V', ['command']);

    // Mock the native CGEvent dispatcher
    jest.spyOn(resolver, 'handleCgEvent')
        .mockResolvedValue(true);

    const result = await resolver.resolve({ type: 'cgevent-cmdv', payload });

    expect(resolver.handleCgEvent).toHaveBeenCalledWith(payload);
    expect(result).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// 3️⃣ AppleScript Attempt
// ---------------------------------------------------------------------------
describe('Resolver – AppleScript Attempt', () => {
  test('executes AppleScript and returns the script result object', async () => {
    const script   = 'tell application "System Events" to keystroke "test"';
    const payload  = utils.buildAppleScriptPayload(script);
    const mockResp = { status: 'success', output: 'script executed' };

    // Mock the AppleScript runner (e.g. `osascript` wrapper)
    jest.spyOn(resolver, 'handleAppleScript')
        .mockResolvedValue(mockResp);

    const result = await resolver.resolve({ type: 'applescript', payload });

    expect(resolver.handleAppleScript).toHaveBeenCalledWith(payload);
    expect(result).toEqual(mockResp);
  });
});