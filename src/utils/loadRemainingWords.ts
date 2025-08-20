import { supabase } from '../services/supabase'

export async function loadRemainingWords() {
  try {
    const { data, error } = await supabase
      .from('spelling_words')
      .select('*')
      .is('definition', null)
      .limit(100)
    
    if (error) throw error
    
    return {
      success: true,
      count: data?.length || 0,
      words: data || []
    }
  } catch (error) {
    console.error('Error loading remaining words:', error)
    return {
      success: false,
      count: 0,
      words: []
    }
  }
}