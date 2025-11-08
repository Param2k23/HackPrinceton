import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  return NextResponse.json({
    success: true,
    message: 'Logged out successfully'
  }, {
    status: 200,
    headers: {
      'Set-Cookie': 'auth_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT'
    }
  });
}