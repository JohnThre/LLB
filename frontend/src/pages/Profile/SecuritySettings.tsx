import React from "react";
import {
  Box,
  TextField,
  Button,
  Grid,
  Typography,
  Divider,
} from "@mui/material";
import { useTranslation } from "react-i18next";

const SecuritySettings: React.FC = () => {
  const { t } = useTranslation();
  const [passwords, setPasswords] = React.useState({
    current: "",
    new: "",
    confirm: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswords((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement password change logic
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h6" gutterBottom>
        {t("security.changePassword")}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label={t("security.currentPassword")}
            name="current"
            type="password"
            value={passwords.current}
            onChange={handleChange}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label={t("security.newPassword")}
            name="new"
            type="password"
            value={passwords.new}
            onChange={handleChange}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label={t("security.confirmPassword")}
            name="confirm"
            type="password"
            value={passwords.confirm}
            onChange={handleChange}
          />
        </Grid>

        <Grid item xs={12}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            size="large"
          >
            {t("security.updatePassword")}
          </Button>
        </Grid>
      </Grid>

      <Divider sx={{ my: 4 }} />

      <Typography variant="h6" gutterBottom>
        {t("security.twoFactor")}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Button variant="outlined" color="primary" size="large" fullWidth>
            {t("security.enable2FA")}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SecuritySettings;
