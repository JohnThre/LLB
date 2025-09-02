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

  const checkBrowserSupport = useCallback(() => {
    if (!isSupported) {
      const error = new AudioPermissionError(
        AudioErrorType.BROWSER_NOT_SUPPORTED,
        'Your browser does not support audio recording'
      );
      handleError(error);
      return false;
    }
    return true;
  }, [isSupported, handleError]);

  const executeWithLoading = useCallback(async <T>(
    action: () => Promise<T>,
    setLastActionFn?: () => void
  ): Promise<T | null> => {
    setIsLoading(true);
    setError(null);
    if (setLastActionFn) setLastActionFn();

    try {
      return await action();
    } catch (err) {
      handleError(err as AudioPermissionError | Error);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [handleError]);

  const refreshCapabilities = useCallback(async () => {
    if (!checkBrowserSupport()) return;

    const caps = await executeWithLoading(async () => {
      const result = await getAudioCapabilities();
      setCapabilities(result);
      if (result.hasPermission && onPermissionGranted) {
        onPermissionGranted();
      }
      return result;
    });
  }, [checkBrowserSupport, executeWithLoading, onPermissionGranted]);

  const requestPermission = useCallback(async (): Promise<boolean> => {
    if (!checkBrowserSupport()) return false;

    const result = await executeWithLoading(async () => {
      const stream = await requestMicrophonePermission();
      stream.getTracks().forEach(track => track.stop());
      await refreshCapabilities();
      if (onPermissionGranted) onPermissionGranted();
      return true;
    }, () => setLastAction(() => requestPermission));

    return result ?? false;
  }, [checkBrowserSupport, executeWithLoading, refreshCapabilities, onPermissionGranted]);

  const testAudio = useCallback(async (): Promise<boolean> => {
    if (!checkBrowserSupport()) return false;
    
    if (!hasPermission) {
      const success = await requestPermission();
      if (!success) return false;
    }

    const result = await executeWithLoading(
      () => testMicrophone(),
      () => setLastAction(() => testAudio)
    );

    return result ?? false;
  }, [checkBrowserSupport, hasPermission, requestPermission, executeWithLoading]);

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