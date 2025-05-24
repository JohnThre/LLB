import { useRef, useCallback, useState, useEffect } from 'react';
import { StreamingVoiceChatRef } from '../components/common/StreamingVoiceChat';

interface UseStreamingVoiceChatOptions {
  language?: string;
  autoPlayResponses?: boolean;
  enableTTS?: boolean;
  chunkDuration?: number;
  maxSessionDuration?: number;
  onError?: (error: string) => void;
  onSessionStart?: (sessionId: string) => void;
  onSessionEnd?: () => void;
}

interface UseStreamingVoiceChatReturn {
  streamingVoiceChatRef: React.RefObject<StreamingVoiceChatRef>;
  isStreamingEnabled: boolean;
  toggleStreaming: () => void;
  generateSpeechResponse: (text: string) => Promise<void>;
  stopAudio: () => void;
  startSession: () => Promise<void>;
  endSession: () => Promise<void>;
  getSessionStats: () => Promise<any>;
  handleVoiceInput: (text: string) => void;
  handleVoiceResponse: (audioUrl: string) => void;
  sessionStatus: 'disconnected' | 'connecting' | 'connected' | 'error';
  isSessionActive: boolean;
}

export const useStreamingVoiceChat = (
  onMessageSend: (message: string) => void,
  options: UseStreamingVoiceChatOptions = {}
): UseStreamingVoiceChatReturn => {
  const {
    language = 'en',
    autoPlayResponses = true,
    enableTTS = true,
    chunkDuration = 2.0,
    maxSessionDuration = 3600,
    onError,
    onSessionStart,
    onSessionEnd
  } = options;

  const streamingVoiceChatRef = useRef<StreamingVoiceChatRef>(null);
  const [isStreamingEnabled, setIsStreamingEnabled] = useState(true);
  const [sessionStatus, setSessionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected');
  const [isSessionActive, setIsSessionActive] = useState(false);

  // Monitor session status
  useEffect(() => {
    const checkSessionStatus = async () => {
      if (streamingVoiceChatRef.current) {
        try {
          const stats = await streamingVoiceChatRef.current.getSessionStats();
          if (stats) {
            setSessionStatus('connected');
            setIsSessionActive(stats.isActive);
          } else {
            setSessionStatus('disconnected');
            setIsSessionActive(false);
          }
        } catch (error) {
          setSessionStatus('error');
          setIsSessionActive(false);
        }
      }
    };

    const interval = setInterval(checkSessionStatus, 5000); // Check every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const toggleStreaming = useCallback(() => {
    setIsStreamingEnabled(prev => !prev);
  }, []);

  const generateSpeechResponse = useCallback(async (text: string) => {
    if (!isStreamingEnabled || !streamingVoiceChatRef.current) return;

    try {
      await streamingVoiceChatRef.current.generateSpeech(text);
    } catch (error) {
      console.error('Streaming voice generation error:', error);
      if (onError) {
        onError('Failed to generate voice response');
      }
    }
  }, [isStreamingEnabled, onError]);

  const stopAudio = useCallback(() => {
    if (streamingVoiceChatRef.current) {
      streamingVoiceChatRef.current.stopAudio();
    }
  }, []);

  const startSession = useCallback(async () => {
    if (!streamingVoiceChatRef.current) return;

    try {
      setSessionStatus('connecting');
      await streamingVoiceChatRef.current.startSession();
      setSessionStatus('connected');
      setIsSessionActive(true);
      
      if (onSessionStart) {
        const stats = await streamingVoiceChatRef.current.getSessionStats();
        if (stats) {
          onSessionStart(stats.sessionId);
        }
      }
    } catch (error) {
      console.error('Failed to start streaming session:', error);
      setSessionStatus('error');
      setIsSessionActive(false);
      
      if (onError) {
        onError('Failed to start streaming session');
      }
    }
  }, [onError, onSessionStart]);

  const endSession = useCallback(async () => {
    if (!streamingVoiceChatRef.current) return;

    try {
      await streamingVoiceChatRef.current.endSession();
      setSessionStatus('disconnected');
      setIsSessionActive(false);
      
      if (onSessionEnd) {
        onSessionEnd();
      }
    } catch (error) {
      console.error('Failed to end streaming session:', error);
      if (onError) {
        onError('Failed to end streaming session');
      }
    }
  }, [onError, onSessionEnd]);

  const getSessionStats = useCallback(async () => {
    if (!streamingVoiceChatRef.current) return null;

    try {
      return await streamingVoiceChatRef.current.getSessionStats();
    } catch (error) {
      console.error('Failed to get session stats:', error);
      if (onError) {
        onError('Failed to get session statistics');
      }
      return null;
    }
  }, [onError]);

  const handleVoiceInput = useCallback((text: string) => {
    // Process voice input and send as message
    if (text.trim()) {
      onMessageSend(text);
    }
  }, [onMessageSend]);

  const handleVoiceResponse = useCallback((audioUrl: string) => {
    // Handle voice response URL (e.g., for analytics or storage)
    console.log('Streaming voice response generated:', audioUrl);
  }, []);

  // Auto-start session when streaming is enabled
  useEffect(() => {
    if (isStreamingEnabled && sessionStatus === 'disconnected') {
      startSession();
    }
  }, [isStreamingEnabled, sessionStatus, startSession]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (isSessionActive) {
        endSession();
      }
    };
  }, [isSessionActive, endSession]);

  return {
    streamingVoiceChatRef,
    isStreamingEnabled,
    toggleStreaming,
    generateSpeechResponse,
    stopAudio,
    startSession,
    endSession,
    getSessionStats,
    handleVoiceInput,
    handleVoiceResponse,
    sessionStatus,
    isSessionActive,
  };
}; 