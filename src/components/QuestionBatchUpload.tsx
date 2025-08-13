'use client';

import React, { useState, useRef } from 'react';

interface BatchUploadResult {
  success: boolean;
  loaded?: number;
  inserted?: number;
  updated?: number;
  deleted?: number;
  errors: string[];
}

export default function QuestionBatchUpload() {
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [result, setResult] = useState<BatchUploadResult | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [jsonInput, setJsonInput] = useState('');
  const [uploadMode, setUploadMode] = useState<'file' | 'json'>('file');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setResult(null);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;

    setUploadStatus('uploading');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('/api/quiz/batch', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      setResult(data);
      setUploadStatus(data.success ? 'success' : 'error');
    } catch (error) {
      setResult({
        success: false,
        errors: [error instanceof Error ? error.message : 'Upload failed'],
      });
      setUploadStatus('error');
    }
  };

  const handleJsonUpload = async () => {
    if (!jsonInput.trim()) return;

    setUploadStatus('uploading');
    setResult(null);

    try {
      let jsonData;
      try {
        jsonData = JSON.parse(jsonInput);
      } catch {
        throw new Error('Invalid JSON format');
      }

      const response = await fetch('/api/quiz/batch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'loadJSON',
          jsonData,
        }),
      });

      const data = await response.json();
      
      setResult(data);
      setUploadStatus(data.success ? 'success' : 'error');
    } catch (error) {
      setResult({
        success: false,
        errors: [error instanceof Error ? error.message : 'Upload failed'],
      });
      setUploadStatus('error');
    }
  };

  const resetUpload = () => {
    setUploadStatus('idle');
    setResult(null);
    setSelectedFile(null);
    setJsonInput('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const downloadTemplate = (format: 'csv' | 'json') => {
    let content: string;
    let mimeType: string;
    let filename: string;

    if (format === 'csv') {
      content = `nodeId,question,option1,option2,option3,option4,correct,explanation
symbols-meaning,What is the primary purpose of symbols?,To represent ideas,To look pretty,To confuse,To take up space,0,Symbols are visual representations of ideas or concepts
patterns-basics,What defines a pattern?,Repetition of elements,Random arrangement,Single occurrence,Chaos,0,Patterns are defined by the repetition of elements in a predictable manner`;
      mimeType = 'text/csv';
      filename = 'quiz_questions_template.csv';
    } else {
      content = JSON.stringify({
        "symbols-meaning": [
          {
            "question": "What is the primary purpose of symbols?",
            "options": ["To represent ideas", "To look pretty", "To confuse", "To take up space"],
            "correct": 0,
            "explanation": "Symbols are visual representations of ideas or concepts"
          }
        ],
        "patterns-basics": [
          {
            "question": "What defines a pattern?",
            "options": ["Repetition of elements", "Random arrangement", "Single occurrence", "Chaos"],
            "correct": 0,
            "explanation": "Patterns are defined by the repetition of elements in a predictable manner"
          }
        ]
      }, null, 2);
      mimeType = 'application/json';
      filename = 'quiz_questions_template.json';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Batch Upload Quiz Questions</h2>

      <div className="mb-6">
        <div className="flex gap-4 mb-4">
          <button
            onClick={() => setUploadMode('file')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              uploadMode === 'file'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Upload File
          </button>
          <button
            onClick={() => setUploadMode('json')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              uploadMode === 'json'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Paste JSON
          </button>
        </div>

        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">Download template:</p>
          <div className="flex gap-2">
            <button
              onClick={() => downloadTemplate('csv')}
              className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
            >
              CSV Template
            </button>
            <button
              onClick={() => downloadTemplate('json')}
              className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 text-sm"
            >
              JSON Template
            </button>
          </div>
        </div>
      </div>

      {uploadMode === 'file' ? (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select File (.csv or .json)
            </label>
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.json"
              onChange={handleFileSelect}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-purple-50 file:text-purple-700
                hover:file:bg-purple-100"
            />
          </div>

          {selectedFile && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-sm text-gray-700">
                Selected: <span className="font-medium">{selectedFile.name}</span>
              </p>
              <p className="text-xs text-gray-500">
                Size: {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
          )}

          <button
            onClick={handleFileUpload}
            disabled={!selectedFile || uploadStatus === 'uploading'}
            className={`px-6 py-2 rounded-lg font-medium transition-colors ${
              !selectedFile || uploadStatus === 'uploading'
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-purple-600 text-white hover:bg-purple-700'
            }`}
          >
            {uploadStatus === 'uploading' ? 'Uploading...' : 'Upload File'}
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Paste JSON Data
            </label>
            <textarea
              value={jsonInput}
              onChange={(e) => setJsonInput(e.target.value)}
              className="w-full h-64 p-3 border border-gray-300 rounded-lg font-mono text-sm"
              placeholder={`Example format:
{
  "node-id-1": [
    {
      "question": "Question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correct": 0,
      "explanation": "Explanation text"
    }
  ]
}`}
            />
          </div>

          <button
            onClick={handleJsonUpload}
            disabled={!jsonInput.trim() || uploadStatus === 'uploading'}
            className={`px-6 py-2 rounded-lg font-medium transition-colors ${
              !jsonInput.trim() || uploadStatus === 'uploading'
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-purple-600 text-white hover:bg-purple-700'
            }`}
          >
            {uploadStatus === 'uploading' ? 'Uploading...' : 'Upload JSON'}
          </button>
        </div>
      )}

      {result && (
        <div className={`mt-6 p-4 rounded-lg ${
          result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        }`}>
          <h3 className={`font-semibold mb-2 ${
            result.success ? 'text-green-800' : 'text-red-800'
          }`}>
            {result.success ? 'Upload Successful' : 'Upload Failed'}
          </h3>
          
          {result.success && (
            <p className="text-green-700">
              Successfully loaded {result.loaded || result.inserted || 0} questions
            </p>
          )}
          
          {result.errors && result.errors.length > 0 && (
            <div className="mt-2">
              <p className="text-red-700 font-medium">Errors:</p>
              <ul className="list-disc list-inside text-sm text-red-600 mt-1">
                {result.errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}

          <button
            onClick={resetUpload}
            className="mt-4 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Upload More
          </button>
        </div>
      )}
    </div>
  );
}