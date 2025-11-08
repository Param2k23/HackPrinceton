import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { email, password } = body;

    // Call the Python backend for authentication
    const backendResponse = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await backendResponse.json();
  // log backend response for debugging
  console.log('[api/auth/login] backend status:', backendResponse.status, 'body:', data);

  if (backendResponse.ok) {
      // Create response with data
      const response = NextResponse.json({
        success: true,
        role: data.role,
        username: data.username,
      });

      // Set the cookie in the response headers (include path to ensure scope)
      response.cookies.set('auth_token', data.token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        path: '/',
        maxAge: 60 * 60 * 24 * 7, // 1 week
      });

      return response;
    } else {
      return NextResponse.json(
        { success: false, message: data.message },
        { status: 401 }
      );
    }
  } catch (error) {
    console.error('Login error:', error);
    return NextResponse.json(
      { success: false, message: 'Internal server error' },
      { status: 500 }
    );
  }
}