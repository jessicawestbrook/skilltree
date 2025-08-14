import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createServerSupabaseClient() {
  const cookieStore = await cookies();
  
  // Debug: Log all cookies to see what's available
  const allCookies = cookieStore.getAll();
  console.log('Available cookies:', allCookies.map(c => c.name));

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          const cookies = cookieStore.getAll();
          console.log('Getting cookies for auth:', cookies.map(c => ({ name: c.name, valueLength: c.value?.length })));
          return cookies;
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) => {
              console.log('Setting cookie:', name);
              cookieStore.set(name, value, options);
            });
          } catch (error) {
            // The `setAll` method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
            console.log('Error setting cookies:', error);
          }
        },
      },
    }
  );
}