import React, { useState, useRef, useCallback } from "react";
import {
  Button,
  IconButton,
  Box,
  Typography,
  CircularProgress,
} from "@mui/material";
import { Mic, Stop, Delete } from "@mui/icons-material";
import { useTheme } from "@mui/material/styles";

interface VoiceInputProps {
  onTranscriptionComplete: (text: string) => void;
  language?: string;
  disabled?: boolean;
}

const VoiceInput: React.FC<VoiceInputProps> = ({
  onTranscriptionComplete,
  language,
  disabled = false,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const theme = useTheme();

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
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

        // Send to backend
        fetch("/api/ai/transcribe", {
          method: "POST",
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {
            onTranscriptionComplete(data.text);
            setIsProcessing(false);
            setAudioBlob(null);
          })
          .catch((error) => {
            console.error("Transcription error:", error);
            setIsProcessing(false);
          });

        // Stop all tracks
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  }, [language, onTranscriptionComplete]);

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

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1,
        p: 1,
        borderRadius: 1,
        bgcolor: theme.palette.background.paper,
      }}
    >
      {!isRecording && !isProcessing && (
        <IconButton
          onClick={startRecording}
          disabled={disabled}
          color="primary"
          size="large"
        >
          <Mic />
        </IconButton>
      )}

      {isRecording && (
        <>
          <IconButton onClick={stopRecording} color="error" size="large">
            <Stop />
          </IconButton>
          <Typography variant="body2" color="text.secondary">
            Recording...
          </Typography>
        </>
      )}

      {isProcessing && (
        <>
          <CircularProgress size={24} />
          <Typography variant="body2" color="text.secondary">
            Processing...
          </Typography>
        </>
      )}

      {audioBlob && !isProcessing && (
        <IconButton onClick={cancelRecording} color="error" size="small">
          <Delete />
        </IconButton>
      )}
    </Box>
  );
};

export default VoiceInput;
