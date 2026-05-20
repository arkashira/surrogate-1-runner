/**
 * Unified API for interacting with multiple LLM agents.
 *
 * This module provides:
 *  - An interface (`LLMProvider`) that any LLM implementation must satisfy.
 *  - A registry (`LLMRegistry`) that holds available providers and a default.
 *  - Helper functions to register providers, set the default, and invoke a
 *    generation request through a unified `generate` method.
 *
 * The design is deliberately lightweight to avoid pulling in heavy runtime
 * dependencies.  Concrete providers (e.g. OpenAI, Anthropic) can be added by
 * implementing the `LLMProvider` interface and registering the instance.
 */

export type LLMResponse = {
  /** The generated text from the LLM. */
  text: string;
  /** Optional raw payload returned by the underlying provider. */
  raw?: any;
};

/**
 * Minimal contract that every LLM agent must implement.
 */
export interface LLMProvider {
  /** Unique name of the provider (e.g. "openai", "anthropic"). */
  readonly name: string;

  /**
   * Generate a completion for the given prompt.
   *
   * @param prompt The user prompt.
   * @param options Provider‑specific options (temperature, maxTokens, …).
   * @returns A promise that resolves to an {@link LLMResponse}.
   */
  generate(prompt: string, options?: Record<string, unknown>): Promise<LLMResponse>;
}

/**
 * Registry that stores providers and offers a unified entry‑point.
 */
export class LLMRegistry {
  /** Map of provider name → provider instance. */
  private providers = new Map<string, LLMProvider>();

  /** Name of the default provider (if any). */
  private defaultProviderName?: string;

  /**
   * Register a new provider. If a provider with the same name already exists,
   * it will be overwritten.
   *
   * @param provider The provider instance to register.
   */
  register(provider: LLMProvider): void {
    this.providers.set(provider.name, provider);
    // Auto‑set the first registered provider as default if none chosen yet.
    if (!this.defaultProviderName) {
      this.defaultProviderName = provider.name;
    }
  }

  /**
   * Set the default provider by name.
   *
   * @param name Name of a previously‑registered provider.
   * @throws If the provider does not exist.
   */
  setDefault(name: string): void {
    if (!this.providers.has(name)) {
      throw new Error(`LLM provider "${name}" is not registered`);
    }
    this.defaultProviderName = name;
  }

  /**
   * Retrieve a provider instance.
   *
   * @param name Optional name; if omitted, the default provider is returned.
   * @throws If the requested provider does not exist or no default is set.
   */
  get(name?: string): LLMProvider {
    const providerName = name ?? this.defaultProviderName;
    if (!providerName) {
      throw new Error('No default LLM provider has been set');
    }
    const provider = this.providers.get(providerName);
    if (!provider) {
      throw new Error(`LLM provider "${providerName}" is not registered`);
    }
    return provider;
  }

  /**
   * Generate a completion using the specified (or default) provider.
   *
   * @param prompt Prompt to send to the LLM.
   * @param options Provider‑specific options.
   * @param providerName Optional explicit provider name; otherwise default is used.
   * @returns The LLM's response.
   */
  async generate(
    prompt: string,
    options?: Record<string, unknown>,
    providerName?: string
  ): Promise<LLMResponse> {
    const provider = this.get(providerName);
    return provider.generate(prompt, options);
  }

  /** List all registered provider names (useful for diagnostics). */
  listProviders(): string[] {
    return Array.from(this.providers.keys());
  }
}

/**
 * Export a singleton registry for application‑wide usage.
 */
export const llm = new LLMRegistry();

/**
 * Convenience wrapper around the singleton registry.
 *
 * Allows callers to simply do:
 *
 *   import { llm, registerProvider, setDefaultProvider, generate } from './api';
 *
 *   registerProvider(myProvider);
 *   setDefaultProvider('myProvider');
 *   const resp = await generate('Hello');
 */
export const registerProvider = (provider: LLMProvider): void => llm.register(provider);
export const setDefaultProvider = (name: string): void => llm.setDefault(name);
export const generate = (
  prompt: string,
  options?: Record<string, unknown>,
  providerName?: string
): Promise<LLMResponse> => llm.generate(prompt, options, providerName);