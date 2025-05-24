import React, { 
  useState, 
  useRef, 
  useCallback, 
  useEffect, 
  forwardRef, 
  useImperativeHandle 
} from "react";
import {
  Button,
  IconButton,
  Box,
  Typography,
  CircularProgress,
  Tooltip,
  Chip,
  Alert,
  LinearProgress,
  Card,
  CardContent,
  Divider,
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
  Refresh,
  SignalWifi4Bar,
  SignalWifiOff,
} from "@mui/icons-material";
import { useTheme } from "@mui/material/styles";

interface StreamingVoiceChatProps {
  onTranscriptionComplete: (text: string) => void;
  onVoiceResponse?: (audioUrl: string) => void;
  language?: string;
  disabled?: boolean;
  autoPlayResponses?: boolean;
  enableTTS?: boolean;
  chunkDuration?: number; // seconds
  maxSessionDuration?: number; // seconds
}

interface StreamingSession {
  sessionId: string;
  websocket: WebSocket | null;
  isConnected: boolean;
  language: string;
  createdAt: number;
  lastActivity: number;
}

interface AudioChunk {
  data: ArrayBuffer;
  index: number;
  timestamp: number;
  isFinal: boolean;
}

interface SessionStats {
  sessionId: string;
  createdAt: number;
  lastActivity: number;
  isActive: boolean;
  language: string;
  conversationEntries: number;
  bufferChunks: number;
  bufferSize: number;
  pendingTranscriptions: number;
  pendingResponses: number;
}

export interface StreamingVoiceChatRef {
  generateSpeech: (text: string) => Promise<void>;
  stopAudio: () => void;
  startSession: () => Promise<void>;
  endSession: () => Promise<void>;
  getSessionStats: () => Promise<SessionStats | null>;
}

const StreamingVoiceChat = forwardRef<StreamingVoiceChatRef, StreamingVoiceChatProps>(({
  onTranscriptionComplete,
  onVoiceResponse,
  language = "en",
  disabled = false,
  autoPlayResponses = true,
  enableTTS = true,
  chunkDuration = 2.0,
  maxSessionDuration = 3600, // 1 hour
}, ref) => {
  // Session management
  const [session, setSession] = useState<StreamingSession | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  
  // Audio recording states
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingProgress, setRecordingProgress] = useState(0);
  
  // Audio playback states
  const [isGeneratingTTS, setIsGeneratingTTS] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [currentAudioUrl, setCurrentAudioUrl] = useState<string | null>(null);
  
  // Settings and status
  const [isMuted, setIsMuted] = useState(false);
  const [sessionStats, setSessionStats] = useState<SessionStats | null>(null);
  const [transcriptionBuffer, setTranscriptionBuffer] = useState<string>("");
  
  // Refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const audioChunksRef = useRef<AudioChunk[]>([]);
  const chunkIndexRef = useRef(0);
  const recordingTimerRef = useRef<number | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  
  const theme = useTheme();

  // Initialize audio context
  useEffect(() => {
    audioRef.current = new Audio();
    audioRef.current.onended = () => {
      setIsPlayingAudio(false);
      setCurrentAudioUrl(null);
    };
    audioRef.current.onerror = () => {
      setConnectionError("Failed to play audio response");
      setIsPlayingAudio(false);
    };

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      endSession();
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  const startSession = useCallback(async () => {
    try {
      setIsConnecting(true);
      setConnectionError(null);

      // Create streaming session
      const response = await fetch("/api/v1/audio-streaming/sessions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ language }),
      });

      if (!response.ok) {
        throw new Error(`Failed to create session: ${response.status}`);
      }

      const data = await response.json();
      const sessionId = data.session_id;

      // Create WebSocket connection
      const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const wsUrl = `${wsProtocol}//${window.location.host}/api/v1/audio-streaming/ws/${sessionId}`;
      
      const websocket = new WebSocket(wsUrl);

      websocket.onopen = () => {
        console.log("WebSocket connected");
        setSession({
          sessionId,
          websocket,
          isConnected: true,
          language,
          createdAt: Date.now(),
          lastActivity: Date.now(),
        });
        setIsConnecting(false);
      };

      websocket.onmessage = (event) => {
        handleWebSocketMessage(JSON.parse(event.data));
      };

      websocket.onclose = () => {
        console.log("WebSocket disconnected");
        setSession(prev => prev ? { ...prev, isConnected: false } : null);
        
        // Attempt reconnection after delay
        if (!disabled) {
          reconnectTimeoutRef.current = setTimeout(() => {
            startSession();
          }, 5000);
        }
      };

      websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
        setConnectionError("WebSocket connection failed");
        setIsConnecting(false);
      };

    } catch (error: any) {
      console.error("Error starting session:", error);
      setConnectionError(error.message);
      setIsConnecting(false);
    }
  }, [language, disabled]);

  const endSession = useCallback(async () => {
    if (!session) return;

    try {
      // Stop recording if active
      if (isRecording) {
        stopRecording();
      }

      // Close WebSocket
      if (session.websocket) {
        session.websocket.close();
      }

      // Close session on server
      await fetch(`/api/v1/audio-streaming/sessions/${session.sessionId}`, {
        method: "DELETE",
      });

      setSession(null);
      setSessionStats(null);
      setTranscriptionBuffer("");

    } catch (error) {
      console.error("Error ending session:", error);
    }
  }, [session, isRecording]);

  const handleWebSocketMessage = useCallback((message: any) => {
    const { type, data, timestamp } = message;

    switch (type) {
      case "connection_established":
        console.log("WebSocket connection established");
        break;

      case "transcription":
        if (data && data.text) {
          setTranscriptionBuffer(prev => prev + " " + data.text);
          
          // If confidence is high enough, send to parent
          if (data.confidence > 0.7) {
            onTranscriptionComplete(data.text);
            setTranscriptionBuffer(""); // Clear buffer after successful transcription
          }
        }
        break;

      case "audio_response":
        if (data && data.audio_data) {
          handleAudioResponse(data);
        }
        break;

      case "chunk_received":
        console.log(`Audio chunk ${data.chunk_index} received`);
        break;

      case "tts_queued":
        setIsGeneratingTTS(true);
        break;

      case "stats_response":
        setSessionStats(data.stats);
        break;

      case "error":
        console.error("WebSocket error:", data.message);
        setConnectionError(data.message);
        break;

      default:
        console.log("Unknown message type:", type);
    }

    // Update last activity
    if (session) {
      setSession(prev => prev ? { ...prev, lastActivity: Date.now() } : null);
    }
  }, [session, onTranscriptionComplete]);

  const handleAudioResponse = useCallback((data: any) => {
    try {
      // Convert hex audio data back to bytes
      const audioBytes = new Uint8Array(
        data.audio_data.match(/.{1,2}/g)?.map((byte: string) => parseInt(byte, 16)) || []
      );

      // Create blob and URL
      const audioBlob = new Blob([audioBytes], { type: "audio/wav" });
      const audioUrl = URL.createObjectURL(audioBlob);

      setCurrentAudioUrl(audioUrl);
      setIsGeneratingTTS(false);

      if (onVoiceResponse) {
        onVoiceResponse(audioUrl);
      }

      if (autoPlayResponses && !isMuted) {
        playAudio(audioUrl);
      }

    } catch (error) {
      console.error("Error handling audio response:", error);
      setConnectionError("Failed to process audio response");
      setIsGeneratingTTS(false);
    }
  }, [autoPlayResponses, isMuted, onVoiceResponse]);

  const startRecording = useCallback(async () => {
    if (!session?.isConnected) {
      await startSession();
      return;
    }

    try {
      setConnectionError(null);
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
        }
      });

      // Initialize audio context for processing
      audioContextRef.current = new AudioContext({ sampleRate: 16000 });
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm;codecs=opus",
      });
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      chunkIndexRef.current = 0;

             mediaRecorder.ondataavailable = async (event) => {
         if (event.data.size > 0) {
           const audioData = await event.data.arrayBuffer();
           const chunk: AudioChunk = {
             data: audioData,
             index: chunkIndexRef.current++,
             timestamp: Date.now(),
             isFinal: false,
           };
           audioChunksRef.current.push(chunk);
           
           // Send chunk immediately for real-time processing
           sendAudioChunk(chunk);
         }
       };

      mediaRecorder.onstop = () => {
        // Send final chunk
        if (audioChunksRef.current.length > 0) {
          const finalChunk = audioChunksRef.current[audioChunksRef.current.length - 1];
          finalChunk.isFinal = true;
          sendAudioChunk(finalChunk);
        }

        // Stop all tracks
        stream.getTracks().forEach((track) => track.stop());
        setIsRecording(false);
        setRecordingProgress(0);
      };

      // Start recording with chunked intervals
      mediaRecorder.start(chunkDuration * 1000); // Convert to milliseconds
      setIsRecording(true);

      // Start progress timer
      let progress = 0;
      recordingTimerRef.current = setInterval(() => {
        progress += 0.1;
        setRecordingProgress(Math.min(progress, 100));
      }, 100);

    } catch (error: any) {
      console.error("Error starting recording:", error);
      setConnectionError("Could not access microphone. Please check permissions.");
    }
  }, [session, chunkDuration]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      
      if (recordingTimerRef.current) {
        clearInterval(recordingTimerRef.current);
        recordingTimerRef.current = null;
      }
    }
  }, [isRecording]);

  const sendAudioChunk = useCallback(async (chunk: AudioChunk) => {
    if (!session?.websocket || session.websocket.readyState !== WebSocket.OPEN) {
      return;
    }

    try {
      // Convert ArrayBuffer to hex string
      const audioData = await chunk.data;
      const uint8Array = new Uint8Array(audioData);
      const hexString = Array.from(uint8Array)
        .map(byte => byte.toString(16).padStart(2, '0'))
        .join('');

      const message = {
        type: "audio_chunk",
        data: {
          audio_data: hexString,
          is_final: chunk.isFinal,
          chunk_index: chunk.index,
        },
        timestamp: chunk.timestamp,
      };

      session.websocket.send(JSON.stringify(message));

    } catch (error) {
      console.error("Error sending audio chunk:", error);
    }
  }, [session]);

  const generateSpeech = useCallback(async (text: string) => {
    if (!enableTTS || !text.trim() || !session?.websocket) return;

    try {
      setConnectionError(null);

      const message = {
        type: "text_request",
        data: {
          text: text,
          language: language,
        },
        timestamp: Date.now(),
      };

      session.websocket.send(JSON.stringify(message));

    } catch (error: any) {
      console.error("TTS error:", error);
      setConnectionError("Failed to generate speech. Please try again.");
    }
  }, [enableTTS, language, session]);

  const playAudio = useCallback((audioUrl: string) => {
    if (!audioRef.current || isMuted) return;

    try {
      audioRef.current.src = audioUrl;
      audioRef.current.play();
      setIsPlayingAudio(true);
    } catch (error) {
      console.error("Audio playback error:", error);
      setConnectionError("Failed to play audio");
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

  const getSessionStats = useCallback(async (): Promise<SessionStats | null> => {
    if (!session?.websocket) return null;

    try {
      const message = {
        type: "control",
        data: {
          command: "stats",
        },
        timestamp: Date.now(),
      };

      session.websocket.send(JSON.stringify(message));
      
      // Return current stats (will be updated via WebSocket)
      return sessionStats;

    } catch (error) {
      console.error("Error getting session stats:", error);
      return null;
    }
  }, [session, sessionStats]);

  // Expose methods to parent components
  useImperativeHandle(ref, () => ({
    generateSpeech,
    stopAudio,
    startSession,
    endSession,
    getSessionStats,
  }), [generateSpeech, stopAudio, startSession, endSession, getSessionStats]);

  return (
    <Card
      sx={{
        borderRadius: 2,
        border: `1px solid ${theme.palette.divider}`,
        bgcolor: theme.palette.background.paper,
      }}
    >
      <CardContent>
        {/* Session Status */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}>
          <Typography variant="h6" component="h3">
            Streaming Voice Chat
          </Typography>
          
          {session?.isConnected ? (
            <Chip
              icon={<SignalWifi4Bar />}
              label="Connected"
              color="success"
              size="small"
            />
          ) : (
            <Chip
              icon={<SignalWifiOff />}
              label={isConnecting ? "Connecting..." : "Disconnected"}
              color={isConnecting ? "warning" : "error"}
              size="small"
            />
          )}
          
          <Chip 
            label={language.toUpperCase()} 
            size="small" 
            color="primary" 
            variant="outlined" 
          />
        </Box>

        {/* Connection Error Alert */}
        {connectionError && (
          <Alert 
            severity="error" 
            onClose={() => setConnectionError(null)}
            sx={{ mb: 2 }}
          >
            {connectionError}
          </Alert>
        )}

        {/* Transcription Buffer */}
        {transcriptionBuffer && (
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              Processing: {transcriptionBuffer}
            </Typography>
          </Alert>
        )}

        {/* Voice Input Section */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
            p: 2,
            borderRadius: 1,
            bgcolor: theme.palette.action.hover,
            mb: 2,
          }}
        >
          {!session?.isConnected && !isConnecting && (
            <Tooltip title="Start streaming session">
              <IconButton
                onClick={startSession}
                disabled={disabled}
                color="primary"
                size="large"
              >
                <Refresh />
              </IconButton>
            </Tooltip>
          )}

          {session?.isConnected && !isRecording && !isProcessing && (
            <Tooltip title="Start voice recording">
              <IconButton
                onClick={startRecording}
                disabled={disabled}
                color="primary"
                size="large"
              >
                <Mic />
              </IconButton>
            </Tooltip>
          )}

          {isRecording && (
            <>
              <Tooltip title="Stop recording">
                <IconButton onClick={stopRecording} color="error" size="large">
                  <Stop />
                </IconButton>
              </Tooltip>
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  🎤 Recording... ({Math.round(recordingProgress)}%)
                </Typography>
                <LinearProgress 
                  variant="determinate" 
                  value={recordingProgress} 
                  sx={{ height: 6, borderRadius: 3 }}
                />
              </Box>
            </>
          )}

          {isProcessing && (
            <>
              <CircularProgress size={24} />
              <Typography variant="body2" color="text.secondary">
                🔄 Processing audio stream...
              </Typography>
            </>
          )}
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Voice Output Section */}
        {enableTTS && (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              p: 2,
              borderRadius: 1,
              bgcolor: theme.palette.action.hover,
              mb: 2,
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
              Streaming TTS: {language.toUpperCase()}
            </Typography>
          </Box>
        )}

        {/* Session Statistics */}
        {sessionStats && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Session Statistics
            </Typography>
            <Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Conversation Entries: {sessionStats.conversationEntries}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Buffer Size: {Math.round(sessionStats.bufferSize / 1024)}KB
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Pending Transcriptions: {sessionStats.pendingTranscriptions}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Pending Responses: {sessionStats.pendingResponses}
              </Typography>
            </Box>
          </Box>
        )}

        {/* Session Controls */}
        <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
          <Button
            variant="outlined"
            size="small"
            onClick={getSessionStats}
            disabled={!session?.isConnected}
          >
            Refresh Stats
          </Button>
          
          <Button
            variant="outlined"
            color="error"
            size="small"
            onClick={endSession}
            disabled={!session}
          >
            End Session
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
});

StreamingVoiceChat.displayName = 'StreamingVoiceChat';

export default StreamingVoiceChat; 