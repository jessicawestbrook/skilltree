import { supabase } from '../services/supabase'

export async function loadSpellingWordsInBatches(words: any[], batchSize: number = 100) {
  const results = []
  
  for (let i = 0; i < words.length; i += batchSize) {
    const batch = words.slice(i, i + batchSize)
    
    try {
      const { data, error } = await supabase
        .from('spelling_words')
        .insert(batch)
        .select()
      
      if (error) {
        console.error(`Error inserting batch ${i / batchSize + 1}:`, error)
        results.push({ batch: i / batchSize + 1, success: false, error })
      } else {
        results.push({ batch: i / batchSize + 1, success: true, count: data?.length || 0 })
      }
    } catch (error) {
      console.error(`Error with batch ${i / batchSize + 1}:`, error)
      results.push({ batch: i / batchSize + 1, success: false, error })
    }
  }
  
  return results
}