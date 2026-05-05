import React from "react";
import { Box } from "@mui/material";
import AppRoutes from "./routes";
import { SnackbarProvider } from "./components/common/SnackbarProvider";
import { AuthProvider } from "./contexts/AuthContext";

const App: React.FC = () => {
  return (
    <Box data-testid="app-container" className="theme-default">
      <AuthProvider>
        <SnackbarProvider>
          <AppRoutes />
        </SnackbarProvider>
      </AuthProvider>
    </Box>
  );
};

export default App;
