/**
 * Tests for AI provider settings.
 */

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import AIProviderSettings from "../../components/Settings/AIProviderSettings";

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (_key: string, fallback?: string) => fallback || _key,
  }),
}));

const saveProviderCredentials = vi.fn();
const localStorageSetItem = vi.fn();

describe("AIProviderSettings", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    Object.defineProperty(window, "llbDesktop", {
      configurable: true,
      value: {
        providerCredentials: {
          save: saveProviderCredentials,
        },
      },
    });
    Object.defineProperty(window, "localStorage", {
      configurable: true,
      value: {
        getItem: vi.fn(),
        setItem: localStorageSetItem,
        removeItem: vi.fn(),
        clear: vi.fn(),
      },
    });
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        providers: [
          {
            name: "openai",
            display_name: "OpenAI",
            default_model: "gpt-5.2",
            models: ["gpt-5.2", "gpt-5-mini"],
            requires_api_key: true,
          },
          {
            name: "mistral",
            display_name: "Mistral AI",
            default_model: "mistral-medium-3.5",
            models: ["mistral-medium-3.5"],
            requires_api_key: true,
          },
        ],
      }),
    } as Response);
  });

  it("renders provider choices from the backend catalog", async () => {
    render(<AIProviderSettings />);

    expect(await screen.findAllByText("OpenAI")).toHaveLength(2);
    expect(screen.getByText("Mistral AI")).toBeInTheDocument();
    expect(screen.getByDisplayValue("gpt-5.2")).toBeInTheDocument();
  });

  it("saves keys through the Electron bridge without local storage", async () => {
    render(<AIProviderSettings />);

    fireEvent.change(await screen.findByLabelText("API key"), {
      target: { value: "sk-user-owned-key" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Save provider key" }));

    await waitFor(() => {
      expect(saveProviderCredentials).toHaveBeenCalledWith({
        openai: {
          api_key: "sk-user-owned-key",
          model: "gpt-5.2",
        },
      });
    });
    expect(localStorageSetItem).not.toHaveBeenCalled();
  });
});
