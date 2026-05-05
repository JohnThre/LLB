import { useRef, useCallback, useState } from 'react';
import { VoiceChatRef } from '../components/common/VoiceChat';

interface UseVoiceChatOptions {
  language?: string;
  autoPlayResponses?: boolean;
  enableTTS?: boolean;
  onError?: (error: string) => void;
}

interface UseVoiceChatReturn {
  voiceChatRef: React.RefObject<VoiceChatRef>;
  isVoiceEnabled: boolean;
  isRecording: boolean;
  isProcessing: boolean;
  transcript: string;
  error: string | null;
  toggleVoice: () => void;
  startRecording: () => Promise<void>;
  stopRecording: () => void;
  clearTranscript: () => void;
  generateSpeechResponse: (text: string) => Promise<void>;
  stopAudio: () => void;
  handleVoiceInput: (text: string) => void;
  handleVoiceResponse: (audioUrl: string) => void;
}

export const useVoiceChat = (
  onMessageSend: (message: string) => void = () => {},
  options: UseVoiceChatOptions = {}
): UseVoiceChatReturn => {
  const {
    language = 'en',
    autoPlayResponses = true,
    enableTTS = true,
    onError
  } = options;

  const voiceChatRef = useRef<VoiceChatRef>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);

  const toggleVoice = useCallback(() => {
    setIsVoiceEnabled(prev => !prev);
  }, []);

  const stopStream = useCallback(() => {
    streamRef.current?.getTracks().forEach(track => track.stop());
    streamRef.current = null;
  }, []);

  const startRecording = useCallback(async () => {
    if (isRecording) return;

    try {
      setError(null);
      setIsProcessing(false);

      if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === 'undefined') {
        throw new Error('Audio recording is not supported in this browser');
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);

      streamRef.current = stream;
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        setIsRecording(false);
        setIsProcessing(false);
        stopStream();
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not start recording');
      setIsRecording(false);
      setIsProcessing(false);
      stopStream();
    }
  }, [isRecording, stopStream]);

  const stopRecording = useCallback(() => {
    const mediaRecorder = mediaRecorderRef.current;

    if (mediaRecorder && isRecording) {
      setIsProcessing(true);
      mediaRecorder.stop();
    }

    setIsRecording(false);
    stopStream();
  }, [isRecording, stopStream]);

  const clearTranscript = useCallback(() => {
    setTranscript('');
  }, []);

  const generateSpeechResponse = useCallback(async (text: string) => {
    if (!isVoiceEnabled || !voiceChatRef.current) return;

    try {
      await voiceChatRef.current.generateSpeech(text);
    } catch (error) {
      console.error('Voice generation error:', error);
      if (onError) {
        onError('Failed to generate voice response');
      }
    }
  }, [isVoiceEnabled, onError]);

  const stopAudio = useCallback(() => {
    if (voiceChatRef.current) {
      voiceChatRef.current.stopAudio();
    }
  }, []);

  const handleVoiceInput = useCallback((text: string) => {
    // Process voice input and send as message
    if (text.trim()) {
      onMessageSend(text);
    }
  }, [onMessageSend]);

  const handleVoiceResponse = useCallback((audioUrl: string) => {
    // Handle voice response URL (e.g., for analytics or storage)
    console.log('Voice response generated:', audioUrl);
  }, []);

  return {
    voiceChatRef,
    isVoiceEnabled,
    isRecording,
    isProcessing,
    transcript,
    error,
    toggleVoice,
    startRecording,
    stopRecording,
    clearTranscript,
    generateSpeechResponse,
    stopAudio,
    handleVoiceInput,
    handleVoiceResponse,
  };
};

export default useVoiceChat;
