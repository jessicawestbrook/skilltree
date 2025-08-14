import { createServerClient } from '@supabase/ssr';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({
            request,
          });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh session if expired - required for Server Components
  const { data: { user } } = await supabase.auth.getUser();

  // Don't block API routes in middleware - let them handle their own auth
  // This allows the API routes to properly read cookies and authenticate
  // Protected routes that require authentication
  // const protectedPaths = ['/api/friends', '/api/progress', '/api/social'];
  // const isProtectedPath = protectedPaths.some(path => request.nextUrl.pathname.startsWith(path));

  // if (isProtectedPath && !user) {
  //   // For API routes, return 401
  //   if (request.nextUrl.pathname.startsWith('/api/')) {
  //     return NextResponse.json(
  //       { error: 'Unauthorized' },
  //       { status: 401 }
  //     );
  //   }
  // }

  return supabaseResponse;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};