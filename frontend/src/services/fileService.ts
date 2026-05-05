import { API_BASE_URL } from "../config";

export interface UploadResponse {
  filename: string;
  fileType: string;
  size: number;
  url: string;
  success?: boolean;
  fileId?: string;
}

type FileCategory = "audio" | "document" | "image";

const MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024;
const ALLOWED_MIME_TYPES = new Set([
  "application/pdf",
  "audio/mpeg",
  "audio/mp3",
  "audio/wav",
  "audio/x-wav",
  "image/png",
  "image/jpeg",
  "text/plain",
]);

const ALLOWED_EXTENSIONS = new Set([
  ".pdf",
  ".mp3",
  ".wav",
  ".png",
  ".jpg",
  ".jpeg",
  ".txt",
]);

export const validateFile = (file: File): boolean => {
  if (!file || file.size > MAX_FILE_SIZE_BYTES) {
    return false;
  }

  const extension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
  return ALLOWED_MIME_TYPES.has(file.type) || ALLOWED_EXTENSIONS.has(extension);
};

const inferFileCategory = (file: File): FileCategory => {
  if (file.type.startsWith("audio/")) return "audio";
  if (file.type.startsWith("image/")) return "image";
  return "document";
};

const toBackendFileType = (fileType: FileCategory): string => {
  if (fileType === "document") return "documents";
  if (fileType === "image") return "images";
  return fileType;
};

const readErrorMessage = async (response: Response): Promise<string> => {
  try {
    const error = await response.json();
    return error.detail || error.message || "Upload failed";
  } catch {
    return "Upload failed";
  }
};

export class FileService {
  private static instance: FileService;
  private baseUrl: string;

  private constructor() {
    this.baseUrl = `${API_BASE_URL}/api/files`;
  }

  public static getInstance(): FileService {
    if (!FileService.instance) {
      FileService.instance = new FileService();
    }
    return FileService.instance;
  }

  async uploadFile(
    file: File,
    fileType: FileCategory = inferFileCategory(file),
  ): Promise<UploadResponse> {
    if (!validateFile(file)) {
      throw new Error("Unsupported file type or file too large");
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", toBackendFileType(fileType));

    try {
      const response = await fetch(`${this.baseUrl}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await readErrorMessage(response));
      }

      return await response.json();
    } catch (error) {
      console.error("File upload error:", error);
      throw error;
    }
  }

  async deleteFile(filename: string, fileType: string): Promise<void> {
    try {
      const response = await fetch(
        `${this.baseUrl}/delete/${fileType}/${filename}`,
        {
          method: "DELETE",
        },
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Delete failed");
      }
    } catch (error) {
      console.error("File delete error:", error);
      throw error;
    }
  }

  getFileUrl(filename: string, fileType: string): string {
    return `${this.baseUrl}/${fileType}/${filename}`;
  }
}

export const fileService = FileService.getInstance();

export const uploadFile = (file: File, fileType?: FileCategory): Promise<UploadResponse> => {
  return fileService.uploadFile(file, fileType);
};
