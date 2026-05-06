import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Chip,
  CircularProgress,
  Link,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import { apiUrl } from "../config";
import { bauhausColors } from "../theme";

interface LiteratureSource {
  id: string;
  title: string;
  publisher: string;
  language: string;
  source_type: string;
  url: string;
  topics: string[];
  excerpt: string;
  status: string;
  jurisdiction: string;
}

const Literature: React.FC = () => {
  const [sources, setSources] = useState<LiteratureSource[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<"approved" | "pending">("approved");
  const [form, setForm] = useState({
    title: "",
    publisher: "",
    url: "",
    topics: "",
    excerpt: "",
  });

  const loadSources = async (status: "approved" | "pending" = statusFilter) => {
    try {
      const response = await fetch(apiUrl(`/api/v1/literature/sources?status=${status}`));
      if (!response.ok) {
        setSources([]);
        return;
      }
      const data = await response.json();
      setSources(data.sources || []);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadSources(statusFilter);
  }, []);

  const handleFormChange = (field: keyof typeof form) => (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setForm((previous) => ({ ...previous, [field]: event.target.value }));
  };

  const submitSource = async (event: React.FormEvent) => {
    event.preventDefault();
    await fetch(apiUrl("/api/v1/literature/sources"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: form.title,
        publisher: form.publisher,
        language: "en",
        source_type: "official",
        url: form.url,
        topics: form.topics.split(",").map((topic) => topic.trim()).filter(Boolean),
        excerpt: form.excerpt,
        jurisdiction: "US",
      }),
    });
    setForm({ title: "", publisher: "", url: "", topics: "", excerpt: "" });
    await loadSources();
  };

  const changeStatusFilter = async (status: "approved" | "pending") => {
    setStatusFilter(status);
    setIsLoading(true);
    await loadSources(status);
  };

  const approveSource = async (sourceId: string) => {
    await fetch(apiUrl(`/api/v1/literature/sources/${sourceId}/approve`), {
      method: "POST",
    });
    await loadSources(statusFilter);
  };

  if (isLoading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ fontWeight: 700, mb: 3 }}>
        Literature
      </Typography>
      <Box sx={{ display: "flex", gap: 1, mb: 3 }}>
        <Button
          variant={statusFilter === "approved" ? "contained" : "outlined"}
          onClick={() => changeStatusFilter("approved")}
          sx={{ borderRadius: 0 }}
        >
          Approved
        </Button>
        <Button
          variant={statusFilter === "pending" ? "contained" : "outlined"}
          onClick={() => changeStatusFilter("pending")}
          sx={{ borderRadius: 0 }}
        >
          Pending
        </Button>
      </Box>
      <Paper
        component="form"
        elevation={0}
        onSubmit={submitSource}
        sx={{
          p: 2,
          mb: 3,
          borderRadius: 0,
          border: `2px solid ${bauhausColors.black}`,
        }}
      >
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
          Submit source
        </Typography>
        <Box sx={{ display: "grid", gap: 2, gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" } }}>
          <TextField label="Title" inputProps={{ "aria-label": "Title" }} value={form.title} onChange={handleFormChange("title")} required />
          <TextField label="Publisher" inputProps={{ "aria-label": "Publisher" }} value={form.publisher} onChange={handleFormChange("publisher")} required />
          <TextField label="URL" inputProps={{ "aria-label": "URL" }} value={form.url} onChange={handleFormChange("url")} required />
          <TextField label="Topics" inputProps={{ "aria-label": "Topics" }} value={form.topics} onChange={handleFormChange("topics")} required />
        </Box>
        <TextField
          label="Excerpt"
          inputProps={{ "aria-label": "Excerpt" }}
          value={form.excerpt}
          onChange={handleFormChange("excerpt")}
          required
          multiline
          minRows={3}
          fullWidth
          sx={{ mt: 2 }}
        />
        <Button
          type="submit"
          variant="contained"
          sx={{
            mt: 2,
            borderRadius: 0,
            backgroundColor: bauhausColors.blue,
            color: bauhausColors.white,
          }}
        >
          Submit source
        </Button>
      </Paper>
      <Box sx={{ display: "grid", gap: 2 }}>
        {sources.map((source) => (
          <Paper
            key={source.id}
            elevation={0}
            sx={{
              p: 2,
              borderRadius: 0,
              border: `2px solid ${bauhausColors.black}`,
              boxShadow: `3px 3px 0 ${bauhausColors.gray[200]}`,
            }}
          >
            <Box sx={{ display: "flex", justifyContent: "space-between", gap: 2, mb: 1 }}>
              <Typography variant="h6" sx={{ fontWeight: 700 }}>
                {source.title}
              </Typography>
              <Chip
                label={source.status}
                size="small"
                sx={{
                  borderRadius: 0,
                  backgroundColor: bauhausColors.yellow,
                  color: bauhausColors.black,
                  fontWeight: 700,
                }}
              />
            </Box>
            <Typography variant="body2" sx={{ color: bauhausColors.gray[700], mb: 1 }}>
              {source.publisher}
            </Typography>
            <Typography variant="caption" sx={{ color: bauhausColors.gray[700], mb: 1, display: "block" }}>
              {source.language} · {source.source_type} · {source.jurisdiction}
            </Typography>
            <Typography variant="body1" sx={{ mb: 2, lineHeight: 1.6 }}>
              {source.excerpt}
            </Typography>
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, mb: 2 }}>
              {source.topics.map((topic) => (
                <Chip key={topic} label={topic} size="small" sx={{ borderRadius: 0 }} />
              ))}
            </Box>
            <Link href={source.url} target="_blank" rel="noopener noreferrer">
              {source.url}
            </Link>
            {source.status === "pending" && (
              <Box sx={{ mt: 2 }}>
                <Button
                  variant="contained"
                  onClick={() => approveSource(source.id)}
                  sx={{ borderRadius: 0, backgroundColor: bauhausColors.blue }}
                >
                  Approve
                </Button>
              </Box>
            )}
          </Paper>
        ))}
      </Box>
    </Box>
  );
};

export default Literature;
