import { NextRequest, NextResponse } from 'next/server';
import { withRateLimit } from '@/lib/rateLimit';

export async function GET(request: NextRequest) {
  return withRateLimit(request, async () => {
    return NextResponse.json({
      success: true,
      message: 'Rate limit test endpoint',
      timestamp: new Date().toISOString()
    });
  }, 'api-strict');
}