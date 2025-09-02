import { createTheme } from "@mui/material/styles";

// Bauhaus color palette - primary colors and functional grays
const bauhausColors = {
  red: "#E53E3E",
  blue: "#2B6CB0", 
  yellow: "#D69E2E",
  black: "#1A202C",
  white: "#FFFFFF",
  gray: {
    50: "#F7FAFC",
    100: "#EDF2F7",
    200: "#E2E8F0",
    300: "#CBD5E0",
    400: "#A0AEC0",
    500: "#718096",
    600: "#4A5568",
    700: "#2D3748",
    800: "#1A202C",
    900: "#171923",
  },
};

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: bauhausColors.blue,
      light: "#4299E1",
      dark: "#2C5282",
      contrastText: bauhausColors.white,
    },
    secondary: {
      main: bauhausColors.red,
      light: "#F56565",
      dark: "#C53030",
      contrastText: bauhausColors.white,
    },
    background: {
      default: bauhausColors.gray[50],
      paper: bauhausColors.white,
    },
    text: {
      primary: bauhausColors.black,
      secondary: bauhausColors.gray[600],
    },
    success: {
      main: "#38A169",
      light: "#48BB78",
      dark: "#2F855A",
    },
    warning: {
      main: bauhausColors.yellow,
      light: "#F6E05E",
      dark: "#B7791F",
    },
    error: {
      main: bauhausColors.red,
      light: "#F56565",
      dark: "#C53030",
    },
    info: {
      main: bauhausColors.blue,
      light: "#4299E1",
      dark: "#2C5282",
    },
  },
  typography: {
    fontFamily: [
      "Futura",
      "Helvetica Neue",
      "Arial",
      "sans-serif",
    ].join(","),
    h1: {
      fontSize: "3rem",
      fontWeight: 700,
      lineHeight: 1.1,
      letterSpacing: "-0.02em",
    },
    h2: {
      fontSize: "2.25rem",
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: "-0.01em",
    },
    h3: {
      fontSize: "1.875rem",
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h4: {
      fontSize: "1.5rem",
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: "1.25rem",
      fontWeight: 500,
      lineHeight: 1.5,
    },
    h6: {
      fontSize: "1.125rem",
      fontWeight: 500,
      lineHeight: 1.5,
    },
    body1: {
      fontSize: "1rem",
      lineHeight: 1.6,
      fontWeight: 400,
    },
    body2: {
      fontSize: "0.875rem",
      lineHeight: 1.5,
      fontWeight: 400,
    },
  },
  shape: {
    borderRadius: 0, // Bauhaus prefers sharp, geometric edges
  },
  shadows: [
    "none",
    "0px 1px 0px rgba(0, 0, 0, 0.1)", // Minimal shadow - Bauhaus prefers clean lines
    "0px 2px 0px rgba(0, 0, 0, 0.1)",
    "0px 3px 0px rgba(0, 0, 0, 0.1)",
    "0px 4px 0px rgba(0, 0, 0, 0.1)",
    "0px 5px 0px rgba(0, 0, 0, 0.1)",
    "0px 6px 0px rgba(0, 0, 0, 0.1)",
    "0px 7px 0px rgba(0, 0, 0, 0.1)",
    "0px 8px 0px rgba(0, 0, 0, 0.1)",
    "0px 9px 0px rgba(0, 0, 0, 0.1)",
    "0px 10px 0px rgba(0, 0, 0, 0.1)",
    "0px 11px 0px rgba(0, 0, 0, 0.1)",
    "0px 12px 0px rgba(0, 0, 0, 0.1)",
    "0px 13px 0px rgba(0, 0, 0, 0.1)",
    "0px 14px 0px rgba(0, 0, 0, 0.1)",
    "0px 15px 0px rgba(0, 0, 0, 0.1)",
    "0px 16px 0px rgba(0, 0, 0, 0.1)",
    "0px 17px 0px rgba(0, 0, 0, 0.1)",
    "0px 18px 0px rgba(0, 0, 0, 0.1)",
    "0px 19px 0px rgba(0, 0, 0, 0.1)",
    "0px 20px 0px rgba(0, 0, 0, 0.1)",
    "0px 21px 0px rgba(0, 0, 0, 0.1)",
    "0px 22px 0px rgba(0, 0, 0, 0.1)",
    "0px 23px 0px rgba(0, 0, 0, 0.1)",
    "0px 24px 0px rgba(0, 0, 0, 0.1)",
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "uppercase",
          borderRadius: 0,
          fontWeight: 700,
          padding: "16px 32px",
          fontSize: "0.875rem",
          letterSpacing: "0.1em",
          border: "2px solid transparent",
          transition: "all 0.15s ease",
          "&:hover": {
            transform: "none",
            boxShadow: "none",
          },
        },
        contained: {
          boxShadow: "none",
          "&:hover": {
            boxShadow: "none",
            filter: "brightness(0.9)",
          },
        },
        outlined: {
          borderWidth: "2px",
          "&:hover": {
            borderWidth: "2px",
            backgroundColor: "transparent",
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 0,
          border: "1px solid",
          borderColor: bauhausColors.gray[200],
        },
        elevation1: {
          boxShadow: "2px 2px 0px rgba(0, 0, 0, 0.1)",
        },
        elevation2: {
          boxShadow: "4px 4px 0px rgba(0, 0, 0, 0.1)",
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: 0,
            backgroundColor: bauhausColors.white,
            "& fieldset": {
              borderWidth: "2px",
              borderColor: bauhausColors.gray[300],
            },
            "&:hover fieldset": {
              borderColor: bauhausColors.gray[400],
            },
            "&.Mui-focused fieldset": {
              borderColor: bauhausColors.blue,
              borderWidth: "2px",
            },
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 0,
          border: "2px solid",
          borderColor: bauhausColors.gray[200],
          boxShadow: "4px 4px 0px rgba(0, 0, 0, 0.1)",
          transition: "all 0.15s ease",
          "&:hover": {
            transform: "translate(-2px, -2px)",
            boxShadow: "6px 6px 0px rgba(0, 0, 0, 0.15)",
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 0,
          fontWeight: 600,
          textTransform: "uppercase",
          fontSize: "0.75rem",
          letterSpacing: "0.05em",
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: "none",
          borderBottom: `3px solid ${bauhausColors.black}`,
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRadius: 0,
          borderRight: `3px solid ${bauhausColors.gray[200]}`,
        },
      },
    },
  },
});

// Export Bauhaus colors for use in components
export { bauhausColors };
export default theme;
