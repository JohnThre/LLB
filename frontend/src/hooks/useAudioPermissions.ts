import { useState, useEffect, useCallback } from 'react';
import {
  AudioCapabilities,
  AudioPermissionError,
  AudioErrorType,
  getAudioCapabilities,
  requestMicrophonePermission,
  testMicrophone,
  isBrowserSupported,
} from '../utils/audioPermissions';

interface UseAudioPermissionsOptions {
  autoCheck?: boolean;
  onPermissionGranted?: () => void;
  onPermissionDenied?: (error: AudioPermissionError) => void;
  onError?: (error: AudioPermissionError | Error) => void;
}

interface UseAudioPermissionsReturn {
  capabilities: AudioCapabilities | null;
  isLoading: boolean;
  error: AudioPermissionError | Error | null;
  hasPermission: boolean;
  isSupported: boolean;
  requestPermission: () => Promise<boolean>;
  testAudio: () => Promise<boolean>;
  refreshCapabilities: () => Promise<void>;
  clearError: () => void;
  retryLastAction: () => Promise<void>;
}

export const useAudioPermissions = (
  options: UseAudioPermissionsOptions = {}
): UseAudioPermissionsReturn => {
  const {
    autoCheck = true,
    onPermissionGranted,
    onPermissionDenied,
    onError,
  } = options;

  const [capabilities, setCapabilities] = useState<AudioCapabilities | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<AudioPermissionError | Error | null>(null);
  const [lastAction, setLastAction] = useState<(() => Promise<boolean | void>) | null>(null);

  const isSupported = isBrowserSupported();
  const hasPermission = capabilities?.hasPermission ?? false;

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const handleError = useCallback((err: AudioPermissionError | Error) => {
    setError(err);
    if (onError) {
      onError(err);
    }
    if (err instanceof AudioPermissionError && err.type === AudioErrorType.PERMISSION_DENIED && onPermissionDenied) {
      onPermissionDenied(err);
    }
  }, [onError, onPermissionDenied]);

  const refreshCapabilities = useCallback(async () => {
    if (!isSupported) {
      const error = new AudioPermissionError(
        AudioErrorType.BROWSER_NOT_SUPPORTED,
        'Your browser does not support audio recording'
      );
      handleError(error);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const caps = await getAudioCapabilities();
      setCapabilities(caps);
      
      if (caps.hasPermission && onPermissionGranted) {
        onPermissionGranted();
      }
    } catch (err) {
      handleError(err as AudioPermissionError | Error);
    } finally {
      setIsLoading(false);
    }
  }, [isSupported, handleError, onPermissionGranted]);

  const requestPermission = useCallback(async (): Promise<boolean> => {
    if (!isSupported) {
      const error = new AudioPermissionError(
        AudioErrorType.BROWSER_NOT_SUPPORTED,
        'Your browser does not support audio recording'
      );
      handleError(error);
      return false;
    }

    setIsLoading(true);
    setError(null);
    setLastAction(() => requestPermission);

    try {
      const stream = await requestMicrophonePermission();
      
      // Stop the stream immediately as we only needed permission
      stream.getTracks().forEach(track => track.stop());
      
      // Refresh capabilities to get updated permission status
      await refreshCapabilities();
      
      if (onPermissionGranted) {
        onPermissionGranted();
      }
      
      return true;
    } catch (err) {
      handleError(err as AudioPermissionError);
      return false;
    } finally {
      setIsLoading(false);
    }
  }, [isSupported, handleError, onPermissionGranted, refreshCapabilities]);

  const testAudio = useCallback(async (): Promise<boolean> => {
    if (!isSupported) {
      const error = new AudioPermissionError(
        AudioErrorType.BROWSER_NOT_SUPPORTED,
        'Your browser does not support audio recording'
      );
      handleError(error);
      return false;
    }

    if (!hasPermission) {
      const success = await requestPermission();
      if (!success) return false;
    }

    setIsLoading(true);
    setError(null);
    setLastAction(() => testAudio);

    try {
      const result = await testMicrophone();
      return result;
    } catch (err) {
      handleError(err as AudioPermissionError);
      return false;
    } finally {
      setIsLoading(false);
    }
  }, [isSupported, hasPermission, requestPermission, handleError]);

  const retryLastAction = useCallback(async () => {
    if (lastAction) {
      await lastAction();
    } else {
      await refreshCapabilities();
    }
  }, [lastAction, refreshCapabilities]);

  // Auto-check capabilities on mount
  useEffect(() => {
    if (autoCheck) {
      refreshCapabilities();
    }
  }, [autoCheck, refreshCapabilities]);

  // Listen for device changes
  useEffect(() => {
    if (!isSupported || !navigator.mediaDevices?.addEventListener) return;

    const handleDeviceChange = () => {
      // Refresh capabilities when devices change
      refreshCapabilities();
    };

    navigator.mediaDevices.addEventListener('devicechange', handleDeviceChange);

    return () => {
      navigator.mediaDevices.removeEventListener('devicechange', handleDeviceChange);
    };
  }, [isSupported, refreshCapabilities]);

  return {
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
  };
}; 