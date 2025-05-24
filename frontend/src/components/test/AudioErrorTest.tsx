import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  Divider,
  Alert,
} from '@mui/material';
import {
  Science,
  Mic,
  VolumeUp,
  Error,
  CheckCircle,
} from '@mui/icons-material';
import { useAudioPermissions } from '../../hooks/useAudioPermissions';
import AudioErrorHandler from '../common/AudioErrorHandler';
import VoiceChat from '../common/VoiceChat';
import {
  AudioPermissionError,
  AudioErrorType,
  testMicrophone,
} from '../../utils/audioPermissions';

const AudioErrorTest: React.FC = () => {
  const [testResults, setTestResults] = useState<Record<string, boolean>>({});
  const [isRunningTests, setIsRunningTests] = useState(false);
  const [currentTest, setCurrentTest] = useState<string | null>(null);

  const {
    capabilities,
    isLoading,
    error,
    hasPermission,
    isSupported,
    requestPermission,
    testAudio,
    refreshCapabilities,
    clearError,
    retryLastAction,
  } = useAudioPermissions({
    autoCheck: true,
    onPermissionGranted: () => {
      console.log('✅ Permission granted');
    },
    onPermissionDenied: (error) => {
      console.log('❌ Permission denied:', error);
    },
    onError: (error) => {
      console.log('🔥 Error occurred:', error);
    },
  });

  const runTest = async (testName: string, testFn: () => Promise<boolean>) => {
    setCurrentTest(testName);
    try {
      const result = await testFn();
      setTestResults(prev => ({ ...prev, [testName]: result }));
      return result;
    } catch (error) {
      console.error(`Test ${testName} failed:`, error);
      setTestResults(prev => ({ ...prev, [testName]: false }));
      return false;
    } finally {
      setCurrentTest(null);
    }
  };

  const runAllTests = async () => {
    setIsRunningTests(true);
    setTestResults({});

    const tests = [
      {
        name: 'Browser Support',
        fn: async () => isSupported,
      },
      {
        name: 'Permission Request',
        fn: async () => {
          try {
            return await requestPermission();
          } catch (error) {
            return false;
          }
        },
      },
      {
        name: 'Microphone Test',
        fn: async () => {
          try {
            return await testMicrophone();
          } catch (error) {
            return false;
          }
        },
      },
      {
        name: 'Audio Capabilities',
        fn: async () => {
          await refreshCapabilities();
          return capabilities?.hasAudioInput ?? false;
        },
      },
      {
        name: 'Voice Recording',
        fn: async () => {
          try {
            return await testAudio();
          } catch (error) {
            return false;
          }
        },
      },
    ];

    for (const test of tests) {
      await runTest(test.name, test.fn);
      // Small delay between tests
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    setIsRunningTests(false);
  };

  const simulateError = (errorType: AudioErrorType) => {
    const errorMessages = {
      [AudioErrorType.PERMISSION_DENIED]: 'Microphone permission denied by user',
      [AudioErrorType.NO_DEVICES]: 'No microphone devices found',
      [AudioErrorType.DEVICE_IN_USE]: 'Microphone is being used by another application',
      [AudioErrorType.BROWSER_NOT_SUPPORTED]: 'Browser does not support audio recording',
      [AudioErrorType.HARDWARE_ERROR]: 'Hardware error occurred',
      [AudioErrorType.NETWORK_ERROR]: 'Network error during audio processing',
      [AudioErrorType.UNKNOWN_ERROR]: 'Unknown error occurred',
      [AudioErrorType.DEVICE_NOT_FOUND]: 'Specified audio device not found',
    };

    // This would normally be set by the actual error, but for testing we simulate it
    console.error('Simulated error:', errorType, errorMessages[errorType]);
  };

  const handleTranscription = (text: string) => {
    console.log('Transcription received:', text);
  };

  const handleVoiceResponse = (audioUrl: string) => {
    console.log('Voice response generated:', audioUrl);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Science />
        Audio Error Handling Test Suite
      </Typography>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        This component tests the improved audio error handling capabilities including 
        microphone permissions, device detection, and error recovery mechanisms.
      </Typography>

      <Grid container spacing={3}>
        {/* Current Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Current Audio Status
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Alert 
                  severity={isSupported ? 'success' : 'error'}
                  icon={isSupported ? <CheckCircle /> : <Error />}
                >
                  Browser Support: {isSupported ? 'Supported' : 'Not Supported'}
                </Alert>

                <Alert 
                  severity={hasPermission ? 'success' : 'warning'}
                  icon={hasPermission ? <CheckCircle /> : <Mic />}
                >
                  Microphone Permission: {hasPermission ? 'Granted' : 'Not Granted'}
                </Alert>

                {capabilities && (
                  <Alert 
                    severity={capabilities.hasAudioInput ? 'success' : 'warning'}
                    icon={capabilities.hasAudioInput ? <CheckCircle /> : <VolumeUp />}
                  >
                    Audio Devices: {capabilities.devices.length} found
                  </Alert>
                )}

                {isLoading && (
                  <Alert severity="info">
                    Loading audio capabilities...
                  </Alert>
                )}
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle2" gutterBottom>
                Supported Constraints:
              </Typography>
              {capabilities?.supportedConstraints && (
                <Box sx={{ fontSize: '0.875rem', fontFamily: 'monospace' }}>
                  {Object.entries(capabilities.supportedConstraints)
                    .filter(([_, supported]) => supported)
                    .map(([constraint]) => constraint)
                    .join(', ')}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Error Handler Demo */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Error Handler Demo
              </Typography>

              {error && (
                <AudioErrorHandler
                  error={error}
                  onRetry={retryLastAction}
                  onDismiss={clearError}
                  showTroubleshooting={true}
                />
              )}

              <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                Simulate Different Errors:
              </Typography>

              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {Object.values(AudioErrorType).map((errorType) => (
                  <Button
                    key={errorType}
                    size="small"
                    variant="outlined"
                    onClick={() => simulateError(errorType)}
                  >
                    {errorType.replace('_', ' ')}
                  </Button>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Test Suite */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Automated Tests
              </Typography>

              <Button
                variant="contained"
                onClick={runAllTests}
                disabled={isRunningTests}
                sx={{ mb: 2 }}
              >
                {isRunningTests ? 'Running Tests...' : 'Run All Tests'}
              </Button>

              {currentTest && (
                <Alert severity="info" sx={{ mb: 2 }}>
                  Running: {currentTest}
                </Alert>
              )}

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                {Object.entries(testResults).map(([testName, passed]) => (
                  <Alert
                    key={testName}
                    severity={passed ? 'success' : 'error'}
                    icon={passed ? <CheckCircle /> : <Error />}
                  >
                    {testName}: {passed ? 'PASSED' : 'FAILED'}
                  </Alert>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Voice Chat Component */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Voice Chat with Error Handling
              </Typography>

              <VoiceChat
                onTranscriptionComplete={handleTranscription}
                onVoiceResponse={handleVoiceResponse}
                language="en"
                enableTTS={true}
                autoPlayResponses={false}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Device Information */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Audio Device Information
              </Typography>

              {capabilities?.devices && capabilities.devices.length > 0 ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {capabilities.devices.map((device, index) => (
                    <Alert key={device.deviceId} severity="info">
                      <strong>Device {index + 1}:</strong> {device.label || 'Unknown Device'} 
                      <br />
                      <small>ID: {device.deviceId}</small>
                    </Alert>
                  ))}
                </Box>
              ) : (
                <Alert severity="warning">
                  No audio input devices detected. This could be due to:
                  <ul>
                    <li>No microphone connected</li>
                    <li>Microphone permission not granted</li>
                    <li>Browser security restrictions</li>
                  </ul>
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AudioErrorTest; 