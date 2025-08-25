import { supabase } from '../services/supabase'

export async function loadSpellingData() {
  try {
    const { data, error } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(100)
    
    if (error) throw error
    
    return { success: data?.length || 0, data }
  } catch (error) {
    console.error('Error loading spelling data:', error)
    throw error
  }
}

export async function checkSpellingData() {
  try {
    const { data, error } = await supabase
      .from('spelling_words')
      .select('*')
      .limit(100)
    
    if (error) throw error
    
    return data || []
  } catch (error) {
    console.error('Error checking spelling data:', error)
    return []
  }
}