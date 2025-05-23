import React from "react";
import { Container } from "@mui/material";
import { Settings as SettingsComponent } from "../components/Settings/Settings";

const Settings: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <SettingsComponent />
    </Container>
  );
};

export default Settings;
