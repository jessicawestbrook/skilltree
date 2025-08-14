import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase-server';

// Remove edge runtime for Node.js features
// export const runtime = 'edge';

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
    version: '0.6.0',
    services: {
      database: 'down',
      api: 'up',
    },
  };

  try {
    // Check database connectivity
    // Use knowledge_nodes table which exists and doesn't require authentication
    const supabase = await createClient();
    const { data, error: dbError } = await supabase
      .from('knowledge_nodes')
      .select('id')
      .limit(1);
    
    if (!dbError) {
      health.services.database = 'up';
    } else {
      console.error('Database health check error:', dbError);
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