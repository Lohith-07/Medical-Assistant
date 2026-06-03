import React from 'react';

interface FileCardProps {
  fileName: string;
  fileSize: string;
  progress: number;
  onRemove: () => void;
}

export const FileCard: React.FC<FileCardProps> = ({
  fileName,
  fileSize,
  progress,
  onRemove,
}) => {
  return (
    <div className="flex flex-col p-4 bg-gray-50 border border-gray-100 rounded-xl gap-2 transition-all hover:shadow-sm">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="text-2xl text-blue-500">📄</div>
          <div className="flex flex-col min-w-0">
            <span className="text-sm font-semibold text-gray-800 truncate" title={fileName}>
              {fileName}
            </span>
            <span className="text-xs text-gray-500">{fileSize}</span>
          </div>
        </div>
        <button
          onClick={onRemove}
          className="text-gray-400 hover:text-red-500 transition-colors p-1 rounded-lg hover:bg-red-50"
          title="Remove file"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {progress < 100 && (
        <div className="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
          <div
            className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
};
