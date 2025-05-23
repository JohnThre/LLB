import React from "react";
import { Box, Typography, Tabs, Tab } from "@mui/material";
import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";

const Profile: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();

  const handleTabChange = (_: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t("profile.title")}
      </Typography>

      <Tabs value={location.pathname} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab
          label={t("profile.settings")}
          value="/dashboard/profile/settings"
        />
        <Tab
          label={t("profile.security")}
          value="/dashboard/profile/security"
        />
      </Tabs>

      <Outlet />
    </Box>
  );
};

export default Profile;
