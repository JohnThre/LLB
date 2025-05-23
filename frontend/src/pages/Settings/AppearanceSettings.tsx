import React from 'react';
import {
  Box,
  Typography,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  SelectChangeEvent,
  RadioGroup,
  FormControlLabel,
  Radio,
} from '@mui/material';
import { useTranslation } from 'react-i18next';

const AppearanceSettings: React.FC = () => {
  const { t } = useTranslation();
  const [settings, setSettings] = React.useState({
    fontSize: 16,
    fontFamily: 'Roboto',
    colorScheme: 'blue',
    density: 'comfortable',
    borderRadius: 4,
  });

  const handleSliderChange = (name: string) => (
    _: Event,
    value: number | number[]
  ) => {
    setSettings((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSelectChange = (name: string) => (
    event: SelectChangeEvent
  ) => {
    setSettings((prev) => ({
      ...prev,
      [name]: event.target.value,
    }));
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t('settings.appearance')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography gutterBottom>
            {t('settings.fontSize')}
          </Typography>
          <Slider
            value={settings.fontSize}
            onChange={handleSliderChange('fontSize')}
            min={12}
            max={24}
            step={1}
            marks
            valueLabelDisplay="auto"
          />
        </Grid>

        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>{t('settings.fontFamily')}</InputLabel>
            <Select
              value={settings.fontFamily}
              onChange={handleSelectChange('fontFamily')}
              label={t('settings.fontFamily')}
            >
              <MenuItem value="Roboto">Roboto</MenuItem>
              <MenuItem value="Arial">Arial</MenuItem>
              <MenuItem value="Helvetica">Helvetica</MenuItem>
              <MenuItem value="Times New Roman">Times New Roman</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>{t('settings.colorScheme')}</InputLabel>
            <Select
              value={settings.colorScheme}
              onChange={handleSelectChange('colorScheme')}
              label={t('settings.colorScheme')}
            >
              <MenuItem value="blue">{t('settings.blue')}</MenuItem>
              <MenuItem value="green">{t('settings.green')}</MenuItem>
              <MenuItem value="purple">{t('settings.purple')}</MenuItem>
              <MenuItem value="orange">{t('settings.orange')}</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>
            {t('settings.density')}
          </Typography>
          <RadioGroup
            value={settings.density}
            onChange={handleSelectChange('density')}
          >
            <FormControlLabel
              value="comfortable"
              control={<Radio />}
              label={t('settings.comfortable')}
            />
            <FormControlLabel
              value="compact"
              control={<Radio />}
              label={t('settings.compact')}
            />
            <FormControlLabel
              value="spacious"
              control={<Radio />}
              label={t('settings.spacious')}
            />
          </RadioGroup>
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>
            {t('settings.borderRadius')}
          </Typography>
          <Slider
            value={settings.borderRadius}
            onChange={handleSliderChange('borderRadius')}
            min={0}
            max={16}
            step={1}
            marks
            valueLabelDisplay="auto"
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default AppearanceSettings; 