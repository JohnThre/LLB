import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1976d2", // Google Blue
      light: "#42a5f5",
      dark: "#1565c0",
      contrastText: "#ffffff",
    },
    secondary: {
      main: "#ff6b35", // Warm accent color
      light: "#ff9068",
      dark: "#c73e1d",
      contrastText: "#ffffff",
    },
    background: {
      default: "#f8fafc",
      paper: "#ffffff",
    },
    text: {
      primary: "#1a202c",
      secondary: "#4a5568",
    },
    success: {
      main: "#48bb78",
      light: "#68d391",
      dark: "#38a169",
    },
    warning: {
      main: "#ed8936",
      light: "#f6ad55",
      dark: "#dd6b20",
    },
    error: {
      main: "#f56565",
      light: "#fc8181",
      dark: "#e53e3e",
    },
    info: {
      main: "#4299e1",
      light: "#63b3ed",
      dark: "#3182ce",
    },
  },
  typography: {
    fontFamily: [
      "Google Sans",
      "Roboto",
      "-apple-system",
      "BlinkMacSystemFont",
      '"Segoe UI"',
      '"Helvetica Neue"',
      "Arial",
      "sans-serif",
    ].join(","),
    h1: {
      fontSize: "2.5rem",
      fontWeight: 600,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: "2rem",
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: "1.5rem",
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h4: {
      fontSize: "1.25rem",
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: "1.125rem",
      fontWeight: 600,
      lineHeight: 1.5,
    },
    h6: {
      fontSize: "1rem",
      fontWeight: 600,
      lineHeight: 1.5,
    },
    body1: {
      fontSize: "1rem",
      lineHeight: 1.6,
    },
    body2: {
      fontSize: "0.875rem",
      lineHeight: 1.6,
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    "none",
    "0px 1px 3px rgba(0, 0, 0, 0.12), 0px 1px 2px rgba(0, 0, 0, 0.24)",
    "0px 3px 6px rgba(0, 0, 0, 0.16), 0px 3px 6px rgba(0, 0, 0, 0.23)",
    "0px 10px 20px rgba(0, 0, 0, 0.19), 0px 6px 6px rgba(0, 0, 0, 0.23)",
    "0px 14px 28px rgba(0, 0, 0, 0.25), 0px 10px 10px rgba(0, 0, 0, 0.22)",
    "0px 19px 38px rgba(0, 0, 0, 0.30), 0px 15px 12px rgba(0, 0, 0, 0.22)",
    "0px 24px 48px rgba(0, 0, 0, 0.35), 0px 19px 19px rgba(0, 0, 0, 0.22)",
    "0px 30px 60px rgba(0, 0, 0, 0.40), 0px 24px 24px rgba(0, 0, 0, 0.22)",
    "0px 36px 72px rgba(0, 0, 0, 0.45), 0px 30px 30px rgba(0, 0, 0, 0.22)",
    "0px 42px 84px rgba(0, 0, 0, 0.50), 0px 36px 36px rgba(0, 0, 0, 0.22)",
    "0px 48px 96px rgba(0, 0, 0, 0.55), 0px 42px 42px rgba(0, 0, 0, 0.22)",
    "0px 54px 108px rgba(0, 0, 0, 0.60), 0px 48px 48px rgba(0, 0, 0, 0.22)",
    "0px 60px 120px rgba(0, 0, 0, 0.65), 0px 54px 54px rgba(0, 0, 0, 0.22)",
    "0px 66px 132px rgba(0, 0, 0, 0.70), 0px 60px 60px rgba(0, 0, 0, 0.22)",
    "0px 72px 144px rgba(0, 0, 0, 0.75), 0px 66px 66px rgba(0, 0, 0, 0.22)",
    "0px 78px 156px rgba(0, 0, 0, 0.80), 0px 72px 72px rgba(0, 0, 0, 0.22)",
    "0px 84px 168px rgba(0, 0, 0, 0.85), 0px 78px 78px rgba(0, 0, 0, 0.22)",
    "0px 90px 180px rgba(0, 0, 0, 0.90), 0px 84px 84px rgba(0, 0, 0, 0.22)",
    "0px 96px 192px rgba(0, 0, 0, 0.95), 0px 90px 90px rgba(0, 0, 0, 0.22)",
    "0px 102px 204px rgba(0, 0, 0, 1.00), 0px 96px 96px rgba(0, 0, 0, 0.22)",
    "0px 108px 216px rgba(0, 0, 0, 1.00), 0px 102px 102px rgba(0, 0, 0, 0.22)",
    "0px 114px 228px rgba(0, 0, 0, 1.00), 0px 108px 108px rgba(0, 0, 0, 0.22)",
    "0px 120px 240px rgba(0, 0, 0, 1.00), 0px 114px 114px rgba(0, 0, 0, 0.22)",
    "0px 126px 252px rgba(0, 0, 0, 1.00), 0px 120px 120px rgba(0, 0, 0, 0.22)",
    "0px 132px 264px rgba(0, 0, 0, 1.00), 0px 126px 126px rgba(0, 0, 0, 0.22)",
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          borderRadius: 12,
          fontWeight: 600,
          padding: "12px 24px",
          fontSize: "0.875rem",
          transition: "all 0.2s ease-in-out",
          "&:hover": {
            transform: "translateY(-1px)",
            boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.15)",
          },
        },
        contained: {
          boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.1)",
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          border: "1px solid rgba(0, 0, 0, 0.05)",
        },
        elevation1: {
          boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.08)",
        },
        elevation2: {
          boxShadow: "0px 4px 16px rgba(0, 0, 0, 0.12)",
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: 12,
            backgroundColor: "#ffffff",
            transition: "all 0.2s ease-in-out",
            "&:hover": {
              boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.08)",
            },
            "&.Mui-focused": {
              boxShadow: "0px 4px 16px rgba(25, 118, 210, 0.15)",
            },
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          border: "1px solid rgba(0, 0, 0, 0.05)",
          transition: "all 0.2s ease-in-out",
          "&:hover": {
            transform: "translateY(-2px)",
            boxShadow: "0px 8px 24px rgba(0, 0, 0, 0.12)",
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
  },
});

export default theme;
