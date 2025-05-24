import React from "react";
import AppRoutes from "./routes";
import { SnackbarProvider } from "./components/common/SnackbarProvider";
import { AuthProvider } from "./contexts/AuthContext";

const App: React.FC = () => {
  return (
    <AuthProvider>
      <SnackbarProvider>
        <AppRoutes />
      </SnackbarProvider>
    </AuthProvider>
  );
};

export default App;
