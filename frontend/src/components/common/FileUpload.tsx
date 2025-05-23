import React, { useCallback, useState } from "react";
import {
  Box,
  Typography,
  CircularProgress,
  IconButton,
  Paper,
} from "@mui/material";
import {
  CloudUpload,
  Delete,
  InsertDriveFile,
  Image,
  Description,
  Audiotrack,
} from "@mui/icons-material";
import { useDropzone } from "react-dropzone";
import { useTheme } from "@mui/material/styles";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  onFileRemove?: () => void;
  accept?: string;
  maxSize?: number;
  disabled?: boolean;
  fileType?: "audio" | "document" | "image";
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  onFileRemove,
  accept,
  maxSize = 50 * 1024 * 1024, // 50MB
  disabled = false,
  fileType = "document",
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const theme = useTheme();

  const getFileIcon = () => {
    switch (fileType) {
      case "audio":
        return <Audiotrack />;
      case "image":
        return <Image />;
      default:
        return <Description />;
    }
  };

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;

      const selectedFile = acceptedFiles[0];
      setError(null);

      // Check file size
      if (selectedFile.size > maxSize) {
        setError(`File size exceeds ${maxSize / (1024 * 1024)}MB limit`);
        return;
      }

      setFile(selectedFile);
      setIsUploading(true);

      try {
        await onFileSelect(selectedFile);
      } catch (err) {
        setError("Error uploading file");
        console.error("Upload error:", err);
      } finally {
        setIsUploading(false);
      }
    },
    [maxSize, onFileSelect],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: accept ? { [accept]: [] } : undefined,
    maxSize,
    disabled: disabled || isUploading,
    multiple: false,
  });

  const handleRemove = () => {
    setFile(null);
    setError(null);
    onFileRemove?.();
  };

  return (
    <Box sx={{ width: "100%" }}>
      {!file ? (
        <Paper
          {...getRootProps()}
          sx={{
            p: 3,
            border: `2px dashed ${
              isDragActive ? theme.palette.primary.main : theme.palette.divider
            }`,
            borderRadius: 1,
            bgcolor: isDragActive
              ? theme.palette.action.hover
              : theme.palette.background.paper,
            cursor: disabled ? "not-allowed" : "pointer",
            opacity: disabled ? 0.7 : 1,
          }}
        >
          <input {...getInputProps()} />
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 1,
            }}
          >
            <CloudUpload
              sx={{
                fontSize: 48,
                color: theme.palette.primary.main,
              }}
            />
            <Typography variant="body1" align="center">
              {isDragActive
                ? "Drop the file here"
                : "Drag and drop a file here, or click to select"}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Max file size: {maxSize / (1024 * 1024)}MB
            </Typography>
          </Box>
        </Paper>
      ) : (
        <Paper
          sx={{
            p: 2,
            display: "flex",
            alignItems: "center",
            gap: 2,
          }}
        >
          <Box sx={{ color: theme.palette.primary.main }}>{getFileIcon()}</Box>
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="body2" noWrap>
              {file.name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {(file.size / 1024).toFixed(1)} KB
            </Typography>
          </Box>
          {isUploading ? (
            <CircularProgress size={24} />
          ) : (
            <IconButton onClick={handleRemove} disabled={disabled} size="small">
              <Delete />
            </IconButton>
          )}
        </Paper>
      )}
      {error && (
        <Typography
          variant="caption"
          color="error"
          sx={{ mt: 1, display: "block" }}
        >
          {error}
        </Typography>
      )}
    </Box>
  );
};

export default FileUpload;
