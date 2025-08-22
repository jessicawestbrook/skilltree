import { supabase } from './supabase'

export interface ImageUploadResult {
  url: string
  path: string
  error?: string
}

class ImageService {
  private bucketName = 'learning-images'

  /**
   * Initialize the storage bucket if it doesn't exist
   */
  async initializeBucket(): Promise<void> {
    try {
      const { data: buckets } = await supabase.storage.listBuckets()
      
      const bucketExists = buckets?.some((bucket: any) => bucket.name === this.bucketName)
      
      if (!bucketExists) {
        const { error } = await supabase.storage.createBucket(this.bucketName, {
          public: true,
          allowedMimeTypes: ['image/png', 'image/jpeg', 'image/gif', 'image/webp', 'image/svg+xml']
        })
        
        if (error && !error.message.includes('already exists')) {
          console.error('Error creating bucket:', error)
        }
      }
    } catch (error) {
      console.error('Error initializing bucket:', error)
    }
  }

  /**
   * Upload an image file to Supabase Storage
   */
  async uploadImage(
    file: File,
    folder: 'questions' | 'content' | 'avatars' = 'content'
  ): Promise<ImageUploadResult> {
    try {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        return { url: '', path: '', error: 'File must be an image' }
      }

      // Validate file size (max 5MB)
      const maxSize = 5 * 1024 * 1024 // 5MB
      if (file.size > maxSize) {
        return { url: '', path: '', error: 'Image must be less than 5MB' }
      }

      // Generate unique filename
      const timestamp = Date.now()
      const randomString = Math.random().toString(36).substring(2, 9)
      const fileExt = file.name.split('.').pop()
      const fileName = `${timestamp}-${randomString}.${fileExt}`
      const filePath = `${folder}/${fileName}`

      // Upload to Supabase Storage
      const { data, error } = await supabase.storage
        .from(this.bucketName)
        .upload(filePath, file, {
          cacheControl: '3600',
          upsert: false
        })

      if (error) {
        console.error('Upload error:', error)
        return { url: '', path: '', error: error.message }
      }

      // Get public URL
      const { data: urlData } = supabase.storage
        .from(this.bucketName)
        .getPublicUrl(data.path)

      return {
        url: urlData.publicUrl,
        path: data.path
      }
    } catch (error) {
      console.error('Error uploading image:', error)
      return { url: '', path: '', error: 'Failed to upload image' }
    }
  }

  /**
   * Upload image from URL (for importing external images)
   */
  async uploadImageFromUrl(
    imageUrl: string,
    folder: 'questions' | 'content' | 'avatars' = 'content'
  ): Promise<ImageUploadResult> {
    try {
      // Fetch the image
      const response = await fetch(imageUrl)
      if (!response.ok) {
        return { url: '', path: '', error: 'Failed to fetch image from URL' }
      }

      const blob = await response.blob()
      
      // Validate content type
      if (!blob.type.startsWith('image/')) {
        return { url: '', path: '', error: 'URL does not point to an image' }
      }

      // Create File object from blob
      const fileName = imageUrl.split('/').pop() || 'image.jpg'
      const file = new File([blob], fileName, { type: blob.type })

      // Use existing upload method
      return this.uploadImage(file, folder)
    } catch (error) {
      console.error('Error uploading from URL:', error)
      return { url: '', path: '', error: 'Failed to fetch or upload image from URL' }
    }
  }

  /**
   * Delete an image from storage
   */
  async deleteImage(path: string): Promise<boolean> {
    try {
      const { error } = await supabase.storage
        .from(this.bucketName)
        .remove([path])

      if (error) {
        console.error('Delete error:', error)
        return false
      }

      return true
    } catch (error) {
      console.error('Error deleting image:', error)
      return false
    }
  }

  /**
   * List images in a folder
   */
  async listImages(folder: string): Promise<string[]> {
    try {
      const { data, error } = await supabase.storage
        .from(this.bucketName)
        .list(folder, {
          limit: 100,
          offset: 0
        })

      if (error) {
        console.error('List error:', error)
        return []
      }

      return data?.map((file: any) => {
        const { data: urlData } = supabase.storage
          .from(this.bucketName)
          .getPublicUrl(`${folder}/${file.name}`)
        return urlData.publicUrl
      }) || []
    } catch (error) {
      console.error('Error listing images:', error)
      return []
    }
  }

  /**
   * Get image dimensions
   */
  async getImageDimensions(file: File): Promise<{ width: number; height: number }> {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = () => {
        resolve({ width: img.width, height: img.height })
      }
      img.onerror = reject
      img.src = URL.createObjectURL(file)
    })
  }

  /**
   * Compress image if needed
   */
  async compressImage(file: File, maxWidth: number = 1200): Promise<File> {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')
        if (!ctx) {
          reject(new Error('Could not get canvas context'))
          return
        }

        // Calculate new dimensions
        let { width, height } = img
        if (width > maxWidth) {
          height = (maxWidth / width) * height
          width = maxWidth
        }

        canvas.width = width
        canvas.height = height

        // Draw and compress
        ctx.drawImage(img, 0, 0, width, height)
        
        canvas.toBlob(
          (blob) => {
            if (blob) {
              const compressedFile = new File([blob], file.name, {
                type: 'image/jpeg',
                lastModified: Date.now()
              })
              resolve(compressedFile)
            } else {
              reject(new Error('Failed to compress image'))
            }
          },
          'image/jpeg',
          0.85 // 85% quality
        )
      }
      img.onerror = reject
      img.src = URL.createObjectURL(file)
    })
  }

  /**
   * Migrate external image URLs to Supabase Storage
   */
  async migrateExternalImages(
    contentType: 'questions' | 'learning_content',
    contentId: string,
    imageUrls: string[]
  ): Promise<string[]> {
    const migratedUrls: string[] = []

    for (const url of imageUrls) {
      // Skip if already a Supabase URL
      if (url.includes('supabase')) {
        migratedUrls.push(url)
        continue
      }

      // Upload to Supabase
      const result = await this.uploadImageFromUrl(
        url,
        contentType === 'questions' ? 'questions' : 'content'
      )

      if (result.url) {
        migratedUrls.push(result.url)
        
        // Update database with new URL
        if (contentType === 'questions') {
          await supabase
            .from('questions')
            .update({ image_url: result.url })
            .eq('id', contentId)
        }
      } else {
        // Keep original URL if migration failed
        migratedUrls.push(url)
      }
    }

    return migratedUrls
  }
}

export const imageService = new ImageService()

// Initialize bucket on service load (commented out - bucket created via SQL)
// imageService.initializeBucket()