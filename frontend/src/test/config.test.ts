import { describe, expect, it } from "vitest";

import { resolveApiBaseUrl } from "../config";

describe("API configuration", () => {
  it("prefers the Electron runtime backend URL when present", () => {
    expect(
      resolveApiBaseUrl({
        llbDesktop: { apiBaseUrl: "http://127.0.0.1:49152" },
      }),
    ).toBe("http://127.0.0.1:49152");
  });

  it("falls back to the development backend URL outside Electron", () => {
    expect(resolveApiBaseUrl({})).toBe("http://localhost:8000");
  });
});
