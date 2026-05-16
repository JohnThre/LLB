import React, { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Chip,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  TextField,
  Typography,
} from "@mui/material";
import { useTranslation } from "react-i18next";

import { apiUrl } from "../../config";

interface ProviderCatalogItem {
  name: string;
  display_name: string;
  default_model: string;
  models: string[];
  requires_api_key: boolean;
}

interface ProviderCatalogResponse {
  providers: ProviderCatalogItem[];
}

const AIProviderSettings: React.FC = () => {
  const { t } = useTranslation();
  const [providers, setProviders] = useState<ProviderCatalogItem[]>([]);
  const [selectedProvider, setSelectedProvider] = useState("");
  const [model, setModel] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    const loadProviders = async () => {
      const response = await fetch(apiUrl("/api/v1/ai/providers"));
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = (await response.json()) as ProviderCatalogResponse;
      setProviders(data.providers);
      if (data.providers.length > 0) {
        setSelectedProvider(data.providers[0].name);
        setModel(data.providers[0].default_model);
      }
    };

    loadProviders().catch((error) => {
      console.error("Error loading AI providers:", error);
      setStatus("Could not load AI providers.");
    });
  }, []);

  const activeProvider = useMemo(
    () => providers.find((provider) => provider.name === selectedProvider),
    [providers, selectedProvider],
  );

  const handleProviderChange = (event: SelectChangeEvent) => {
    const nextProvider = providers.find(
      (provider) => provider.name === event.target.value,
    );
    setSelectedProvider(event.target.value);
    setModel(nextProvider?.default_model || "");
    setApiKey("");
    setStatus(null);
  };

  const handleSave = async () => {
    if (!selectedProvider || !model) return;
    if (!window.llbDesktop?.providerCredentials?.save) {
      setStatus(
        t(
          "settings.aiProviders.desktopOnly",
          "Provider keys can be saved in the desktop app.",
        ),
      );
      return;
    }

    await window.llbDesktop.providerCredentials.save({
      [selectedProvider]: {
        api_key: apiKey,
        model,
      },
    });
    setApiKey("");
    setStatus(t("settings.aiProviders.saved", "Provider key saved."));
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        {t("settings.aiProviders.title", "AI Providers")}
      </Typography>

      <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 2 }}>
        {providers.map((provider) => (
          <Chip
            key={provider.name}
            label={provider.display_name}
            size="small"
          />
        ))}
      </Box>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>
              {t("settings.aiProviders.provider", "Provider")}
            </InputLabel>
            <Select
              value={selectedProvider}
              onChange={handleProviderChange}
              label={t("settings.aiProviders.provider", "Provider")}
            >
              {providers.map((provider) => (
                <MenuItem key={provider.name} value={provider.name}>
                  {provider.display_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label={t("settings.aiProviders.model", "Model")}
            value={model}
            onChange={(event) => setModel(event.target.value)}
          />
        </Grid>

        {activeProvider?.requires_api_key && (
          <Grid item xs={12}>
            <TextField
              fullWidth
              label={t("settings.aiProviders.apiKey", "API key")}
              value={apiKey}
              onChange={(event) => setApiKey(event.target.value)}
              type="password"
              autoComplete="off"
            />
          </Grid>
        )}
      </Grid>

      {status && (
        <Alert severity="info" sx={{ mt: 2 }}>
          {status}
        </Alert>
      )}

      <Box sx={{ mt: 2, display: "flex", justifyContent: "flex-end" }}>
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={!selectedProvider || !model}
        >
          {t("settings.aiProviders.saveKey", "Save provider key")}
        </Button>
      </Box>
    </Box>
  );
};

export default AIProviderSettings;
