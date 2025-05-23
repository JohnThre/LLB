import { API_BASE_URL } from "../config";

export interface UploadResponse {
  filename: string;
  fileType: string;
  size: number;
  url: string;
}

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
    fileType: "audio" | "document" | "image",
  ): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("fileType", fileType);

    try {
      const response = await fetch(`${this.baseUrl}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Upload failed");
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
