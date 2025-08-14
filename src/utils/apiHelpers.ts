/**
 * Safe JSON parsing utility to handle HTML error responses
 */
export async function safeJsonParse(response: Response): Promise<any> {
  try {
    const text = await response.text();
    
    // Check if response is HTML (common when getting error pages)
    if (text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
      console.error('Received HTML response instead of JSON:', {
        status: response.status,
        statusText: response.statusText,
        url: response.url,
        htmlSnippet: text.substring(0, 200) + '...'
      });
      
      throw new Error(`API returned HTML instead of JSON. Status: ${response.status} ${response.statusText}`);
    }
    
    // Check if response is empty
    if (!text.trim()) {
      console.warn('Received empty response from API:', {
        status: response.status,
        statusText: response.statusText,
        url: response.url
      });
      
      return null;
    }
    
    // Try to parse as JSON
    return JSON.parse(text);
  } catch (error) {
    console.error('Failed to parse JSON response:', {
      error: error instanceof Error ? error.message : error,
      status: response.status,
      statusText: response.statusText,
      url: response.url
    });
    
    throw new Error(`Invalid JSON response from API: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Enhanced fetch wrapper with better error handling
 */
export async function safeFetch(url: string, options?: RequestInit): Promise<any> {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    // Check if the response is ok
    if (!response.ok) {
      const errorText = await response.text();
      
      // Try to parse error as JSON first
      try {
        const errorJson = JSON.parse(errorText);
        throw new Error(errorJson.message || errorJson.error || `HTTP ${response.status}: ${response.statusText}`);
      } catch {
        // If not JSON, throw with the text content
        throw new Error(`HTTP ${response.status}: ${response.statusText}${errorText ? ` - ${errorText}` : ''}`);
      }
    }

    return await safeJsonParse(response);
  } catch (error) {
    console.error('Fetch failed:', {
      url,
      error: error instanceof Error ? error.message : error,
      options
    });
    
    throw error;
  }
}

/**
 * Retry fetch with exponential backoff
 */
export async function retryFetch(
  url: string, 
  options?: RequestInit, 
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<any> {
  let lastError: Error;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await safeFetch(url, options);
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      
      if (attempt === maxRetries) {
        break;
      }
      
      // Exponential backoff
      const delay = baseDelay * Math.pow(2, attempt);
      console.warn(`Fetch attempt ${attempt + 1} failed, retrying in ${delay}ms:`, lastError.message);
      
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError!;
}