/**
 * Unit tests for src/config/datadog-sandbox.js
 * 
 * Verifies environment variable parsing, default values, edge cases, and immutability.
 */

const path = require("path");

// Helper to require the config after setting env vars
function loadConfig() {
  // Clear module cache to force re-evaluation with new env
  delete require.cache[require.resolve("../../src/config/datadog-sandbox.js")];
  return require("../../src/config/datadog-sandbox.js");
}

describe("Datadog Sandbox Config", () => {
  const ORIGINAL_ENV = { ...process.env };

  afterEach(() => {
    process.env = { ...ORIGINAL_ENV };
  });

  test("uses defaults when env vars are absent", () => {
    delete process.env.DATADOG_SANDBOX_MODE;
    delete process.env.DATADOG_ERROR_RATE;
    const cfg = loadConfig();
    expect(cfg.sandboxMode).toBe(false);
    expect(cfg.errorRate).toBe(0.0);
  });

  test("parses DATADOG_SANDBOX_MODE as true", () => {
    process.env.DATADOG_SANDBOX_MODE = "true";
    const cfg = loadConfig();
    expect(cfg.sandboxMode).toBe(true);
  });

  test("parses DATADOG_SANDBOX_MODE as false", () => {
    process.env.DATADOG_SANDBOX_MODE = "false";
    const cfg = loadConfig();
    expect(cfg.sandboxMode).toBe(false);
  });

  test("trims whitespace in sandbox mode", () => {
    process.env.DATADOG_SANDBOX_MODE = "  true  ";
    const cfg = loadConfig();
    expect(cfg.sandboxMode).toBe(true);
  });

  test("parses valid error rate", () => {
    process.env.DATADOG_ERROR_RATE = "0.25";
    const cfg = loadConfig();
    expect(cfg.errorRate).toBeCloseTo(0.25);
  });

  test("falls back to default for non-numeric error rate", () => {
    process.env.DATADOG_ERROR_RATE = "not-a-number";
    const cfg = loadConfig();
    expect(cfg.errorRate).toBe(0.0);
  });

  test("falls back to default for negative error rate", () => {
    process.env.DATADOG_ERROR_RATE = "-0.5";
    const cfg = loadConfig();
    expect(cfg.errorRate).toBe(0.0);
  });

  test("falls back to default for error rate > 1", () => {
    process.env.DATADOG_ERROR_RATE = "1.5";
    const cfg = loadConfig();
    expect(cfg.errorRate).toBe(0.0);
  });

  test("accepts boundary values 0 and 1 for error rate", () => {
    process.env.DATADOG_ERROR_RATE = "0";
    expect(loadConfig().errorRate).toBe(0);
    
    process.env.DATADOG_ERROR_RATE = "1";
    expect(loadConfig().errorRate).toBe(1);
  });

  test("is immutable (frozen)", () => {
    const cfg = loadConfig();
    expect(() => {
      cfg.sandboxMode = true;
    }).toThrow();
    expect(() => {
      cfg.errorRate = 0.5;
    }).toThrow();
  });
});