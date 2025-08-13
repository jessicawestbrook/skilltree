import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export const runtime = 'edge';

interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  services: {
    database: 'up' | 'down';
    api: 'up' | 'down';
    storage?: 'up' | 'down';
  };
  metrics?: {
    uptime: number;
    responseTime: number;
    memoryUsage?: number;
  };
}

export async function GET() {
  const startTime = Date.now();
  
  const health: HealthStatus = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || '0.1.0',
    services: {
      database: 'down',
      api: 'up',
    },
  };

  try {
    // Check database connectivity
    const { error: dbError } = await supabase
      .from('profiles')
      .select('count')
      .limit(1)
      .single();
    
    if (!dbError) {
      health.services.database = 'up';
    }
    
    // Add metrics
    health.metrics = {
      uptime: process.uptime ? process.uptime() : 0,
      responseTime: Date.now() - startTime,
    };
    
    // Determine overall health status
    if (health.services.database === 'down') {
      health.status = 'degraded';
    }
    
    const statusCode = health.status === 'healthy' ? 200 : 
                       health.status === 'degraded' ? 503 : 500;
    
    return NextResponse.json(health, { status: statusCode });
  } catch (error) {
    health.status = 'unhealthy';
    health.services.database = 'down';
    
    return NextResponse.json(health, { status: 500 });
  }
}