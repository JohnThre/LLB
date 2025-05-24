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
  toggleVoice: () => void;
  generateSpeechResponse: (text: string) => Promise<void>;
  stopAudio: () => void;
  handleVoiceInput: (text: string) => void;
  handleVoiceResponse: (audioUrl: string) => void;
}

export const useVoiceChat = (
  onMessageSend: (message: string) => void,
  options: UseVoiceChatOptions = {}
): UseVoiceChatReturn => {
  const {
    language = 'en',
    autoPlayResponses = true,
    enableTTS = true,
    onError
  } = options;

  const voiceChatRef = useRef<VoiceChatRef>(null);
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(true);

  const toggleVoice = useCallback(() => {
    setIsVoiceEnabled(prev => !prev);
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
    toggleVoice,
    generateSpeechResponse,
    stopAudio,
    handleVoiceInput,
    handleVoiceResponse,
  };
}; 