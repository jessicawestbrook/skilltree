import { createClient } from '@supabase/supabase-js';
import { cookies } from 'next/headers';

export async function createServerSupabaseClient() {
  const cookieStore = await cookies();
  
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      auth: {
        persistSession: false
      }
    }
  );

  // Get the session from cookies if available
  const token = cookieStore.get('sb-access-token')?.value;
  if (token) {
    await supabase.auth.setSession({
      access_token: token,
      refresh_token: cookieStore.get('sb-refresh-token')?.value || ''
    });
  }

  return supabase;
}