import React from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Avatar,
  Typography,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../contexts/AuthContext';

const ProfileSettings: React.FC = () => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [formData, setFormData] = React.useState({
    name: user?.name || '',
    email: user?.email || '',
    bio: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement profile update logic
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Grid container spacing={3}>
        <Grid item xs={12} display="flex" justifyContent="center">
          <Avatar
            sx={{ width: 100, height: 100, mb: 2 }}
            alt={formData.name}
          />
        </Grid>
        
        <Grid item xs={12}>
          <TextField
            fullWidth
            label={t('profile.name')}
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label={t('profile.email')}
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label={t('profile.bio')}
            name="bio"
            multiline
            rows={4}
            value={formData.bio}
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
            {t('common.save')}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProfileSettings; 