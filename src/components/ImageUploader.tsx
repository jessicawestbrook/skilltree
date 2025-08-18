import React, { useState, useRef } from 'react'
import { PhotoIcon, XMarkIcon, ArrowUpTrayIcon, LinkIcon } from '@heroicons/react/24/outline'
import { imageService } from '../services/imageService'

interface ImageUploaderProps {
  onImageUploaded: (url: string) => void
  currentImageUrl?: string
  folder?: 'questions' | 'content' | 'avatars'
  maxSizeMB?: number
  className?: string
}

const ImageUploader: React.FC<ImageUploaderProps> = ({
  onImageUploaded,
  currentImageUrl,
  folder = 'content',
  maxSizeMB = 5,
  className = ''
}) => {
  const [isUploading, setIsUploading] = useState(false)
  const [preview, setPreview] = useState<string>(currentImageUrl || '')
  const [error, setError] = useState<string>('')
  const [showUrlInput, setShowUrlInput] = useState(false)
  const [urlInput, setUrlInput] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setError('')

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file')
      return
    }

    // Validate file size
    const maxSize = maxSizeMB * 1024 * 1024
    if (file.size > maxSize) {
      setError(`Image must be less than ${maxSizeMB}MB`)
      return
    }

    // Show preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target?.result as string)
    }
    reader.readAsDataURL(file)

    // Upload image
    setIsUploading(true)
    try {
      // Compress if needed
      let fileToUpload = file
      if (file.size > 1024 * 1024) { // If larger than 1MB, compress
        fileToUpload = await imageService.compressImage(file, 1200)
      }

      const result = await imageService.uploadImage(fileToUpload, folder)
      
      if (result.error) {
        setError(result.error)
        setPreview('')
      } else {
        onImageUploaded(result.url)
        setPreview(result.url)
      }
    } catch (err) {
      setError('Failed to upload image')
      setPreview('')
    } finally {
      setIsUploading(false)
    }
  }

  const handleUrlSubmit = async () => {
    if (!urlInput.trim()) return

    setError('')
    setIsUploading(true)

    try {
      const result = await imageService.uploadImageFromUrl(urlInput, folder)
      
      if (result.error) {
        setError(result.error)
      } else {
        onImageUploaded(result.url)
        setPreview(result.url)
        setUrlInput('')
        setShowUrlInput(false)
      }
    } catch (err) {
      setError('Failed to upload image from URL')
    } finally {
      setIsUploading(false)
    }
  }

  const handleRemove = () => {
    setPreview('')
    setError('')
    onImageUploaded('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      const event = {
        target: { files: [file] }
      } as unknown as React.ChangeEvent<HTMLInputElement>
      handleFileSelect(event)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {!preview ? (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-lg p-6 text-center hover:border-primary-500 transition-colors"
        >
          <PhotoIcon className="h-12 w-12 text-neutral-400 mx-auto mb-4" />
          
          <div className="space-y-2">
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Drop an image here or click to upload
            </p>
            
            <div className="flex gap-2 justify-center">
              <label className="cursor-pointer">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                  disabled={isUploading}
                />
                <span className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
                  <ArrowUpTrayIcon className="h-4 w-4" />
                  Choose File
                </span>
              </label>
              
              <button
                onClick={() => setShowUrlInput(!showUrlInput)}
                className="inline-flex items-center gap-2 px-4 py-2 bg-neutral-200 dark:bg-neutral-700 rounded-lg hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
              >
                <LinkIcon className="h-4 w-4" />
                From URL
              </button>
            </div>
            
            <p className="text-xs text-neutral-500">
              Max size: {maxSizeMB}MB. Formats: JPG, PNG, GIF, WebP
            </p>
          </div>

          {showUrlInput && (
            <div className="mt-4 flex gap-2">
              <input
                type="url"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="Enter image URL..."
                className="flex-1 px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <button
                onClick={handleUrlSubmit}
                disabled={!urlInput.trim() || isUploading}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Upload
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="relative">
          <img
            src={preview}
            alt="Uploaded"
            className="w-full max-h-64 object-contain rounded-lg bg-neutral-100 dark:bg-neutral-800"
          />
          <button
            onClick={handleRemove}
            className="absolute top-2 right-2 p-2 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors"
            title="Remove image"
          >
            <XMarkIcon className="h-4 w-4" />
          </button>
        </div>
      )}

      {isUploading && (
        <div className="flex items-center justify-center gap-2 text-primary-600">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
          <span className="text-sm">Uploading...</span>
        </div>
      )}

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}
    </div>
  )
}

export default ImageUploader