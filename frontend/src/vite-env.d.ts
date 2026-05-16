/// <reference types="vite/client" />

interface Window {
  llbDesktop?: {
    apiBaseUrl?: string;
    providerCredentials?: {
      save: (
        credentials: Record<string, Record<string, string>>,
      ) => Promise<void>;
    };
  };
}
