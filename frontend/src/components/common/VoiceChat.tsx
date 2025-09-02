import React, { useState, useRef, useCallback, useEffect, forwardRef, useImperativeHandle } from "react";
import {
  Button,
  IconButton,
  Box,
  Typography,
  CircularProgress,
  Tooltip,
  Chip,
  Alert,
} from "@mui/material";
import {
  Mic,
  Stop,
  Delete,
  VolumeUp,
  VolumeOff,
  Settings,
  PlayArrow,
  Pause,
} from "@mui/icons-material";
import { useTheme } from "@mui/material/styles";
import { useAudioPermissions } from "../../hooks/useAudioPermissions";
import AudioErrorHandler from "./AudioErrorHandler";
import {
  AudioPermissionError,
  AudioErrorType,
  requestMicrophonePermission,
} from "../../utils/audioPermissions";

interface VoiceChatProps {
  onTranscriptionComplete: (text: string) => void;
  onVoiceResponse?: (audioUrl: string) => void;
  language?: string;
  disabled?: boolean;
  autoPlayResponses?: boolean;
  enableTTS?: boolean;
}

interface TTSResponse {
  success: boolean;
  audio_url?: string;
  duration?: number;
  language: string;
}

export interface VoiceChatRef {
  generateSpeech: (text: string) => Promise<void>;
  stopAudio: () => void;
}

const VoiceChat = forwardRef<VoiceChatRef, VoiceChatProps>(({
  onTranscriptionComplete,
  onVoiceResponse,
  language = "en",
  disabled = false,
  autoPlayResponses = true,
  enableTTS = true,
}, ref) => {
  // Voice input states
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  
  // Voice output states
  const [isGeneratingTTS, setIsGeneratingTTS] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [currentAudioUrl, setCurrentAudioUrl] = useState<string | null>(null);
  
  // Settings
  const [isMuted, setIsMuted] = useState(false);
  const [transcriptionError, setTranscriptionError] = useState<string | null>(null);
  
  // Refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const theme = useTheme();

  // Memoized audio permissions options to prevent unnecessary re-renders
  const audioPermissionsOptions = React.useMemo(() => ({
    autoCheck: true,
    onPermissionGranted: () => {
      console.log('Microphone permission granted');
    },
    onPermissionDenied: (error: AudioPermissionError) => {
      const sanitizedError = typeof error === 'string' 
        ? error.replace(/[\r\n\t]/g, ' ').substring(0, 200)
        : String(error).replace(/[\r\n\t]/g, ' ').substring(0, 200);
      console.warn('Microphone permission denied:', sanitizedError);
    },
  }), []);

  // Audio permissions hook
  const {
    error: permissionError,
    hasPermission,
    isSupported,
    requestPermission,
    clearError,
    retryLastAction,
  } = useAudioPermissions(audioPermissionsOptions);

  // Initialize audio element
  useEffect(() => {
    audioRef.current = new Audio();
    audioRef.current.onended = () => {
      setIsPlayingAudio(false);
      setCurrentAudioUrl(null);
    };
    audioRef.current.onerror = () => {
      setTranscriptionError("Failed to play audio response");
      setIsPlayingAudio(false);
    };

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  const startRecording = useCallback(async () => {
    try {
      setTranscriptionError(null);
      clearError();

      // Check if we have permission, request if needed
      if (!hasPermission) {
        const granted = await requestPermission();
        if (!granted) {
          return;
        }
      }

      const stream = await requestMicrophonePermission({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: "audio/wav" });
        setAudioBlob(audioBlob);
        setIsProcessing(true);

        // Create form data
        const formData = new FormData();
        formData.append("file", audioBlob, "recording.wav");
        if (language) {
          formData.append("language", language);
        }

        // Send to backend for transcription
        fetch("/api/ai/transcribe", {
          method: "POST",
          body: formData,
        })
          .then(async (response) => {
            if (!response.ok) {
              const errorData = await response.json().catch(() => ({}));
              throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            onTranscriptionComplete(data.text);
            setIsProcessing(false);
            setAudioBlob(null);
          })
          .catch((error) => {
            console.error("Transcription error:", error);
            setTranscriptionError(
              error.message.includes('status: 400') 
                ? "Invalid audio format. Please try recording again."
                : error.message.includes('status: 503')
                ? "Audio service is temporarily unavailable. Please try again later."
                : "Failed to transcribe audio. Please try again."
            );
            setIsProcessing(false);
          });

        // Stop all tracks
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.onerror = (event) => {
        console.error("MediaRecorder error:", event);
        setTranscriptionError("Recording failed. Please try again.");
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      
      if (error instanceof AudioPermissionError) {
        // Error will be handled by the AudioErrorHandler component
        return;
      }
      
      setTranscriptionError("Could not access microphone. Please check permissions.");
    }
  }, [language, onTranscriptionComplete, hasPermission, requestPermission, clearError]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

  const cancelRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setAudioBlob(null);
    }
  }, [isRecording]);

  const generateSpeech = useCallback(async (text: string) => {
    if (!enableTTS || !text.trim()) return;

    try {
      setTranscriptionError(null);
      setIsGeneratingTTS(true);

      const response = await fetch("/api/ai/text-to-speech", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
          language: language,
          voice_settings: {
            rate: 150,
            volume: isMuted ? 0 : 0.8,
          },
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data: TTSResponse = await response.json();

      if (data.success && data.audio_url) {
        setCurrentAudioUrl(data.audio_url);
        
        if (onVoiceResponse) {
          onVoiceResponse(data.audio_url);
        }

        if (autoPlayResponses && !isMuted) {
          playAudio(data.audio_url);
        }
      } else {
        throw new Error("TTS generation failed");
      }
    } catch (error: any) {
      console.error("TTS error:", error);
      setTranscriptionError(
        error.message.includes('status: 503')
          ? "Text-to-speech service is temporarily unavailable."
          : "Failed to generate speech. Please try again."
      );
    } finally {
      setIsGeneratingTTS(false);
    }
  }, [enableTTS, language, isMuted, autoPlayResponses, onVoiceResponse]);

  const playAudio = useCallback((audioUrl: string) => {
    if (!audioRef.current || isMuted) return;

    try {
      audioRef.current.src = audioUrl;
      audioRef.current.play();
      setIsPlayingAudio(true);
    } catch (error) {
      console.error("Audio playback error:", error);
      setTranscriptionError("Failed to play audio");
    }
  }, [isMuted]);

  const stopAudio = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlayingAudio(false);
    }
  }, []);

  const toggleMute = useCallback(() => {
    setIsMuted(!isMuted);
    if (audioRef.current) {
      audioRef.current.muted = !isMuted;
    }
  }, [isMuted]);

  const handleRetryPermission = useCallback(async () => {
    clearError();
    setTranscriptionError(null);
    await retryLastAction();
  }, [clearError, retryLastAction]);

  const handleDismissError = useCallback(() => {
    clearError();
    setTranscriptionError(null);
  }, [clearError]);

  // Expose methods to parent components
  useImperativeHandle(ref, () => ({
    generateSpeech,
    stopAudio,
  }), [generateSpeech, stopAudio]);

  // Show browser not supported message
  if (!isSupported) {
    return (
      <Box sx={{ p: 2 }}>
        <AudioErrorHandler
          error={new AudioPermissionError(
            AudioErrorType.BROWSER_NOT_SUPPORTED,
            'Your browser does not support audio recording'
          )}
          onDismiss={handleDismissError}
          showTroubleshooting={true}
        />
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 1,
        p: 2,
        borderRadius: 2,
        bgcolor: theme.palette.background.paper,
        border: `1px solid ${theme.palette.divider}`,
      }}
    >
      {/* Permission Error Handler */}
      {permissionError && (
        <AudioErrorHandler
          error={permissionError}
          onRetry={handleRetryPermission}
          onDismiss={handleDismissError}
          showTroubleshooting={true}
        />
      )}

      {/* Transcription Error Alert */}
      {transcriptionError && (
        <Alert 
          severity="error" 
          onClose={() => setTranscriptionError(null)}
          sx={{ mb: 1 }}
        >
          {transcriptionError}
        </Alert>
      )}

      {/* Voice Input Section */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1,
          p: 1,
          borderRadius: 1,
          bgcolor: theme.palette.action.hover,
        }}
      >
        {!isRecording && !isProcessing && (
          <Tooltip title={hasPermission ? "Start voice recording" : "Grant microphone permission first"}>
            <span>
              <IconButton
                onClick={startRecording}
                disabled={disabled || !isSupported}
                color="primary"
                size="large"
              >
                <Mic />
              </IconButton>
            </span>
          </Tooltip>
        )}

        {isRecording && (
          <>
            <Tooltip title="Stop recording">
              <IconButton onClick={stopRecording} color="error" size="large">
                <Stop />
              </IconButton>
            </Tooltip>
            <Typography variant="body2" color="text.secondary">
              🎤 Recording...
            </Typography>
            <Chip 
              label={language.toUpperCase()} 
              size="small" 
              color="primary" 
              variant="outlined" 
            />
          </>
        )}

        {isProcessing && (
          <>
            <CircularProgress size={24} />
            <Typography variant="body2" color="text.secondary">
              🔄 Processing speech...
            </Typography>
          </>
        )}

        {audioBlob && !isProcessing && (
          <Tooltip title="Cancel recording">
            <IconButton onClick={cancelRecording} color="error" size="small">
              <Delete />
            </IconButton>
          </Tooltip>
        )}
      </Box>

      {/* Voice Output Section */}
      {enableTTS && (
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
            p: 1,
            borderRadius: 1,
            bgcolor: theme.palette.action.hover,
          }}
        >
          <Tooltip title={isMuted ? "Unmute audio" : "Mute audio"}>
            <IconButton onClick={toggleMute} color="primary">
              {isMuted ? <VolumeOff /> : <VolumeUp />}
            </IconButton>
          </Tooltip>

          {isGeneratingTTS && (
            <>
              <CircularProgress size={20} />
              <Typography variant="body2" color="text.secondary">
                🔊 Generating speech...
              </Typography>
            </>
          )}

          {isPlayingAudio && (
            <>
              <Tooltip title="Stop audio">
                <IconButton onClick={stopAudio} color="error" size="small">
                  <Pause />
                </IconButton>
              </Tooltip>
              <Typography variant="body2" color="text.secondary">
                🔊 Playing response...
              </Typography>
            </>
          )}

          {currentAudioUrl && !isPlayingAudio && !isGeneratingTTS && (
            <Tooltip title="Replay audio">
              <IconButton 
                onClick={() => playAudio(currentAudioUrl)} 
                color="primary" 
                size="small"
              >
                <PlayArrow />
              </IconButton>
            </Tooltip>
          )}

          <Typography variant="caption" color="text.secondary">
            TTS: {language.toUpperCase()}
          </Typography>
        </Box>
      )}
    </Box>
  );
});

VoiceChat.displayName = 'VoiceChat';

export default VoiceChat; 