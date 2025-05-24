import React from 'react';
import {
  Alert,
  AlertTitle,
  Box,
  Button,
  Collapse,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  IconButton,
} from '@mui/material';
import {
  ExpandMore,
  ExpandLess,
  Mic,
  Settings,
  Refresh,
  Help,
  Warning,
  Error as ErrorIcon,
  Info,
} from '@mui/icons-material';
import { useState } from 'react';
import { 
  AudioPermissionError, 
  AudioErrorType, 
  getErrorMessage, 
  getTroubleshootingSteps 
} from '../../utils/audioPermissions';

interface AudioErrorHandlerProps {
  error: AudioPermissionError | Error | null;
  onRetry?: () => void;
  onDismiss?: () => void;
  showTroubleshooting?: boolean;
}

const AudioErrorHandler: React.FC<AudioErrorHandlerProps> = ({
  error,
  onRetry,
  onDismiss,
  showTroubleshooting = true,
}) => {
  const [showSteps, setShowSteps] = useState(false);

  if (!error) return null;

  const isAudioError = error instanceof AudioPermissionError;
  const errorMessage = getErrorMessage(error);
  const troubleshootingSteps = getTroubleshootingSteps(error);

  const getSeverity = () => {
    if (isAudioError) {
      switch (error.type) {
        case AudioErrorType.PERMISSION_DENIED:
          return 'warning';
        case AudioErrorType.BROWSER_NOT_SUPPORTED:
          return 'error';
        case AudioErrorType.NO_DEVICES:
          return 'info';
        default:
          return 'error';
      }
    }
    return 'error';
  };

  const getIcon = () => {
    if (isAudioError) {
      switch (error.type) {
        case AudioErrorType.PERMISSION_DENIED:
          return <Mic />;
        case AudioErrorType.BROWSER_NOT_SUPPORTED:
          return <ErrorIcon />;
        case AudioErrorType.NO_DEVICES:
          return <Settings />;
        default:
          return <Warning />;
      }
    }
    return <ErrorIcon />;
  };

  const getTitle = () => {
    if (isAudioError) {
      switch (error.type) {
        case AudioErrorType.PERMISSION_DENIED:
          return 'Microphone Permission Required';
        case AudioErrorType.BROWSER_NOT_SUPPORTED:
          return 'Browser Not Supported';
        case AudioErrorType.NO_DEVICES:
          return 'No Microphone Found';
        case AudioErrorType.DEVICE_IN_USE:
          return 'Microphone In Use';
        case AudioErrorType.HARDWARE_ERROR:
          return 'Microphone Error';
        default:
          return 'Audio Error';
      }
    }
    return 'Audio Error';
  };

  return (
    <Alert 
      severity={getSeverity()}
      onClose={onDismiss}
      icon={getIcon()}
      sx={{ mb: 2 }}
    >
      <AlertTitle>{getTitle()}</AlertTitle>
      <Typography variant="body2" sx={{ mb: 1 }}>
        {errorMessage}
      </Typography>

      <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
        {onRetry && (
          <Button
            size="small"
            variant="outlined"
            startIcon={<Refresh />}
            onClick={onRetry}
          >
            Try Again
          </Button>
        )}

        {showTroubleshooting && troubleshootingSteps.length > 0 && (
          <Button
            size="small"
            variant="text"
            startIcon={showSteps ? <ExpandLess /> : <ExpandMore />}
            onClick={() => setShowSteps(!showSteps)}
          >
            {showSteps ? 'Hide' : 'Show'} Help
          </Button>
        )}
      </Box>

      {showTroubleshooting && (
        <Collapse in={showSteps}>
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1, display: 'flex', alignItems: 'center' }}>
              <Help sx={{ mr: 1, fontSize: 16 }} />
              Troubleshooting Steps:
            </Typography>
            <List dense>
              {troubleshootingSteps.map((step, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    <Typography variant="caption" color="primary">
                      {index + 1}.
                    </Typography>
                  </ListItemIcon>
                  <ListItemText 
                    primary={step}
                    primaryTypographyProps={{ variant: 'body2' }}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </Collapse>
      )}
    </Alert>
  );
};

export default AudioErrorHandler; 