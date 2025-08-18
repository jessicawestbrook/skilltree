import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables!')
  console.error('Please set REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY')
  
  // Provide a more helpful error message
  throw new Error(
    'Supabase configuration is missing. Please add REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY to your environment variables.'
  )
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)