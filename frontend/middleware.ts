import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { verifyAuth } from '@/lib/auth';
 
export async function middleware(request: NextRequest) {
  // Exclude authentication routes
  if (
    request.nextUrl.pathname.startsWith('/api/auth/login') ||
    request.nextUrl.pathname.startsWith('/api/auth/verify') ||
    request.nextUrl.pathname === '/'
  ) {
    return NextResponse.next();
  }

  try {
    // Verify authentication
    await verifyAuth();
    return NextResponse.next();
  } catch (error) {
    // Redirect to login page
    return NextResponse.redirect(new URL('/', request.url));
  }
}