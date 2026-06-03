import React, { useState, useRef } from 'react';
import { FileCard } from './FileCard';
import { Button } from './Button';

interface FileUploadState {
  id: string;
  file: File;
  name: string;
  size: string;
  progress: number;
}

export const UploadSection: React.FC = () => {
  const [files, setFiles] = useState<FileUploadState[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleFiles = (selectedFiles: FileList | null) => {
    if (!selectedFiles) return;

    const newFiles: FileUploadState[] = [];
    for (let i = 0; i < selectedFiles.length; i++) {
      const file = selectedFiles[i];
      if (file.type !== 'application/pdf') {
        alert('Only PDF files are supported.');
        continue;
      }
      
      const fileId = `${file.name}-${Date.now()}-${i}`;
      newFiles.push({
        id: fileId,
        file,
        name: file.name,
        size: formatFileSize(file.size),
        progress: 0,
      });

      // Simulate upload progress
      let currentProgress = 0;
      const interval = setInterval(() => {
        currentProgress += 10;
        setFiles(prev =>
          prev.map(f => (f.id === fileId ? { ...f, progress: currentProgress } : f))
        );
        if (currentProgress >= 100) {
          clearInterval(interval);
        }
      }, 150);
    }

    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleRemoveFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleClearDatabase = () => {
    setFiles([]);
    alert('Database cleared successfully.');
  };

  const handleProcessFiles = () => {
    if (files.length === 0) return;
    alert(`Processing ${files.length} file(s) for the AI assistant...`);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Section Title */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <span>📁</span> Document Database
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          Upload and manage medical PDFs for the AI clinical assistant.
        </p>
      </div>

      {/* Main Card */}
      <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-8 flex flex-col gap-6">
        {/* Dropzone */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleUploadClick}
          className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all duration-200 ${
            isDragOver
              ? 'border-blue-500 bg-blue-50/50 scale-[1.01] shadow-inner'
              : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50/50'
          }`}
        >
          {/* Upload Icon */}
          <div className={`text-5xl mb-4 transition-transform duration-200 ${isDragOver ? 'scale-110' : ''}`}>
            📤
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-1">
            Upload Medical PDFs
          </h3>
          <p className="text-sm text-gray-500 mb-4">
            Drag & drop PDFs here or browse files
          </p>
          <span className="text-xs text-gray-400">
            Supports multiple PDF files up to 200MB each
          </span>

          <input
            ref={fileInputRef}
            id="pdf-upload"
            type="file"
            accept=".pdf"
            multiple
            className="hidden"
            onChange={e => handleFiles(e.target.files)}
          />
        </div>

        {/* Uploaded File List */}
        {files.length > 0 && (
          <div className="flex flex-col gap-3 max-h-[300px] overflow-y-auto pr-1">
            <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
              Selected Files ({files.length})
            </h4>
            {files.map(file => (
              <FileCard
                key={file.id}
                fileName={file.name}
                fileSize={file.size}
                progress={file.progress}
                onRemove={() => handleRemoveFile(file.id)}
              />
            ))}
          </div>
        )}

        {/* Bottom Actions */}
        <div className="flex items-center justify-end gap-4 border-t border-gray-100 pt-6">
          <Button
            variant="danger-outline"
            onClick={handleClearDatabase}
            disabled={files.length === 0}
            className={files.length === 0 ? 'opacity-50 cursor-not-allowed hover:scale-100' : ''}
          >
            🧹 Clear Database
          </Button>
          <Button
            variant="primary"
            onClick={handleProcessFiles}
            disabled={files.length === 0}
            className={files.length === 0 ? 'opacity-50 cursor-not-allowed hover:scale-100' : ''}
          >
            🚀 Upload Files
          </Button>
        </div>
      </div>
    </div>
  );
};
export default UploadSection;
