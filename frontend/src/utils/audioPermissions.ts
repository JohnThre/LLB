/**
 * Audio Permissions and Device Management Utility
 * Handles microphone permissions, device detection, and error handling
 */

export interface AudioDevice {
  deviceId: string;
  label: string;
  kind: MediaDeviceKind;
}

export interface AudioPermissionStatus {
  granted: boolean;
  denied: boolean;
  prompt: boolean;
  error?: string;
}

export interface AudioCapabilities {
  hasAudioInput: boolean;
  hasPermission: boolean;
  devices: AudioDevice[];
  supportedConstraints: MediaTrackSupportedConstraints;
}

export enum AudioErrorType {
  PERMISSION_DENIED = 'PERMISSION_DENIED',
  NO_DEVICES = 'NO_DEVICES',
  DEVICE_NOT_FOUND = 'DEVICE_NOT_FOUND',
  DEVICE_IN_USE = 'DEVICE_IN_USE',
  HARDWARE_ERROR = 'HARDWARE_ERROR',
  BROWSER_NOT_SUPPORTED = 'BROWSER_NOT_SUPPORTED',
  NETWORK_ERROR = 'NETWORK_ERROR',
  UNKNOWN_ERROR = 'UNKNOWN_ERROR'
}

export class AudioPermissionError extends Error {
  constructor(
    public type: AudioErrorType,
    message: string,
    public originalError?: Error
  ) {
    super(message);
    this.name = 'AudioPermissionError';
  }
}

/**
 * Check if the browser supports audio recording
 */
export function isBrowserSupported(): boolean {
  return !!(
    navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia &&
    typeof MediaRecorder !== 'undefined'
  );
}

/**
 * Get current permission status for microphone
 */
export async function getPermissionStatus(): Promise<AudioPermissionStatus> {
  if (!navigator.permissions) {
    return { granted: false, denied: false, prompt: true };
  }

  try {
    const permission = await navigator.permissions.query({ name: 'microphone' as PermissionName });
    return {
      granted: permission.state === 'granted',
      denied: permission.state === 'denied',
      prompt: permission.state === 'prompt'
    };
  } catch (error) {
    console.warn('Permission API not supported:', error);
    return { granted: false, denied: false, prompt: true };
  }
}

/**
 * Get available audio input devices
 */
export async function getAudioDevices(): Promise<AudioDevice[]> {
  if (!navigator.mediaDevices?.enumerateDevices) {
    throw new AudioPermissionError(
      AudioErrorType.BROWSER_NOT_SUPPORTED,
      'Browser does not support device enumeration'
    );
  }

  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    return devices
      .filter(device => device.kind === 'audioinput')
      .map(device => ({
        deviceId: device.deviceId,
        label: device.label || `Microphone ${device.deviceId.slice(0, 8)}`,
        kind: device.kind
      }));
  } catch (error) {
    throw new AudioPermissionError(
      AudioErrorType.HARDWARE_ERROR,
      'Failed to enumerate audio devices',
      error as Error
    );
  }
}

/**
 * Request microphone permission with detailed error handling
 */
export async function requestMicrophonePermission(
  constraints: MediaStreamConstraints = { audio: true }
): Promise<MediaStream> {
  if (!isBrowserSupported()) {
    throw new AudioPermissionError(
      AudioErrorType.BROWSER_NOT_SUPPORTED,
      'Your browser does not support audio recording. Please use Chrome, Firefox, or Safari.'
    );
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    return stream;
  } catch (error) {
    const err = error as DOMException;
    
    switch (err.name) {
      case 'NotAllowedError':
      case 'PermissionDeniedError':
        throw new AudioPermissionError(
          AudioErrorType.PERMISSION_DENIED,
          'Microphone permission denied. Please allow microphone access in your browser settings.'
        );
      
      case 'NotFoundError':
      case 'DevicesNotFoundError':
        throw new AudioPermissionError(
          AudioErrorType.NO_DEVICES,
          'No microphone found. Please connect a microphone and try again.'
        );
      
      case 'NotReadableError':
      case 'TrackStartError':
        throw new AudioPermissionError(
          AudioErrorType.DEVICE_IN_USE,
          'Microphone is already in use by another application. Please close other apps using the microphone.'
        );
      
      case 'OverconstrainedError':
      case 'ConstraintNotSatisfiedError':
        throw new AudioPermissionError(
          AudioErrorType.DEVICE_NOT_FOUND,
          'No microphone meets the specified requirements. Please check your audio settings.'
        );
      
      case 'NotSupportedError':
        throw new AudioPermissionError(
          AudioErrorType.BROWSER_NOT_SUPPORTED,
          'Audio recording is not supported in this browser or context.'
        );
      
      case 'AbortError':
        throw new AudioPermissionError(
          AudioErrorType.HARDWARE_ERROR,
          'Audio recording was aborted. Please try again.'
        );
      
      default:
        throw new AudioPermissionError(
          AudioErrorType.UNKNOWN_ERROR,
          `Audio access failed: ${err.message || 'Unknown error'}`,
          err
        );
    }
  }
}

/**
 * Get comprehensive audio capabilities
 */
export async function getAudioCapabilities(): Promise<AudioCapabilities> {
  const capabilities: AudioCapabilities = {
    hasAudioInput: false,
    hasPermission: false,
    devices: [],
    supportedConstraints: {}
  };

  if (!isBrowserSupported()) {
    return capabilities;
  }

  try {
    // Get supported constraints
    capabilities.supportedConstraints = navigator.mediaDevices.getSupportedConstraints();

    // Check permission status
    const permissionStatus = await getPermissionStatus();
    capabilities.hasPermission = permissionStatus.granted;

    // Get devices (may require permission)
    try {
      capabilities.devices = await getAudioDevices();
      capabilities.hasAudioInput = capabilities.devices.length > 0;
    } catch (error) {
      // If we can't get devices, try to request permission first
      if (!capabilities.hasPermission) {
        try {
          const stream = await requestMicrophonePermission();
          stream.getTracks().forEach(track => track.stop());
          capabilities.hasPermission = true;
          capabilities.devices = await getAudioDevices();
          capabilities.hasAudioInput = capabilities.devices.length > 0;
        } catch (permError) {
          // Permission denied or other error
          console.warn('Could not get audio capabilities:', permError);
        }
      }
    }
  } catch (error) {
    console.error('Error getting audio capabilities:', error);
  }

  return capabilities;
}

/**
 * Test microphone functionality
 */
export async function testMicrophone(
  deviceId?: string,
  duration: number = 1000
): Promise<boolean> {
  try {
    const constraints: MediaStreamConstraints = {
      audio: deviceId ? { deviceId: { exact: deviceId } } : true
    };

    const stream = await requestMicrophonePermission(constraints);
    
    // Test recording for a short duration
    const mediaRecorder = new MediaRecorder(stream);
    let hasData = false;

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        mediaRecorder.stop();
        stream.getTracks().forEach(track => track.stop());
        resolve(hasData);
      }, duration);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          hasData = true;
        }
      };

      mediaRecorder.onerror = (error) => {
        clearTimeout(timeout);
        stream.getTracks().forEach(track => track.stop());
        reject(new AudioPermissionError(
          AudioErrorType.HARDWARE_ERROR,
          'Microphone test failed',
          error.error
        ));
      };

      mediaRecorder.start();
    });
  } catch (error) {
    throw error;
  }
}

/**
 * Get user-friendly error message for audio errors
 */
export function getErrorMessage(error: AudioPermissionError | Error): string {
  if (error instanceof AudioPermissionError) {
    switch (error.type) {
      case AudioErrorType.PERMISSION_DENIED:
        return 'Please allow microphone access in your browser settings and refresh the page.';
      
      case AudioErrorType.NO_DEVICES:
        return 'No microphone detected. Please connect a microphone and try again.';
      
      case AudioErrorType.DEVICE_IN_USE:
        return 'Your microphone is being used by another application. Please close other apps and try again.';
      
      case AudioErrorType.BROWSER_NOT_SUPPORTED:
        return 'Your browser does not support audio recording. Please use Chrome, Firefox, or Safari.';
      
      case AudioErrorType.HARDWARE_ERROR:
        return 'There was a problem with your microphone. Please check your audio settings.';
      
      default:
        return error.message || 'An unknown audio error occurred. Please try again.';
    }
  }
  
  return error.message || 'An unexpected error occurred.';
}

/**
 * Get troubleshooting steps for audio errors
 */
export function getTroubleshootingSteps(error: AudioPermissionError | Error): string[] {
  if (error instanceof AudioPermissionError) {
    switch (error.type) {
      case AudioErrorType.PERMISSION_DENIED:
        return [
          'Click the microphone icon in your browser\'s address bar',
          'Select "Allow" for microphone access',
          'Refresh the page and try again',
          'Check your browser\'s privacy settings'
        ];
      
      case AudioErrorType.NO_DEVICES:
        return [
          'Connect a microphone to your computer',
          'Check that your microphone is properly plugged in',
          'Test your microphone in other applications',
          'Restart your browser'
        ];
      
      case AudioErrorType.DEVICE_IN_USE:
        return [
          'Close other applications that might be using your microphone',
          'Check for video calls or recording software',
          'Restart your browser',
          'Restart your computer if the problem persists'
        ];
      
      case AudioErrorType.BROWSER_NOT_SUPPORTED:
        return [
          'Use Google Chrome, Mozilla Firefox, or Safari',
          'Update your browser to the latest version',
          'Enable JavaScript in your browser',
          'Try using an incognito/private window'
        ];
      
      default:
        return [
          'Refresh the page and try again',
          'Check your microphone settings',
          'Restart your browser',
          'Contact support if the problem persists'
        ];
    }
  }
  
  return [
    'Refresh the page and try again',
    'Check your internet connection',
    'Contact support if the problem persists'
  ];
} 