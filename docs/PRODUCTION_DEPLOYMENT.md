# Production Deployment Guide

This guide covers deploying NeuroQuest to production using Docker and monitoring setup.

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured
- SSL certificates (for HTTPS)
- GitHub repository with secrets configured

## Deployment Options

### Option 1: Docker Compose (Recommended for Single Server)

#### 1. Prepare Environment Variables

Create a `.env.production` file:

```bash
# Copy from .env.local and update values
cp .env.local .env.production
```

Update production values:
```env
NODE_ENV=production
NEXT_PUBLIC_SUPABASE_URL=your_production_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_production_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_production_service_key
DATABASE_URL=your_production_database_url
REDIS_URL=redis://redis:6379
SENTRY_DSN=your_sentry_dsn
SENTRY_ENABLED=true
OTEL_ENABLED=true
```

#### 2. Deploy with Docker Compose

```bash
# Pull latest code
git pull origin main

# Build and start services
docker-compose -f docker-compose.yml up -d --build

# Check logs
docker-compose logs -f app

# Verify health
curl http://localhost:3000/api/health
```

#### 3. Access Services

- **Application**: http://localhost:3000
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **OpenTelemetry**: http://localhost:4318

### Option 2: Cloud Platform Deployment

#### Deploy to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel --prod
```

3. Set environment variables in Vercel Dashboard

#### Deploy to Railway

1. Connect GitHub repository
2. Add environment variables
3. Deploy with:
```bash
railway up
```

#### Deploy to Google Cloud Run

1. Build container:
```bash
docker build -t gcr.io/your-project/neuroquest:latest .
docker push gcr.io/your-project/neuroquest:latest
```

2. Deploy:
```bash
gcloud run deploy neuroquest \
  --image gcr.io/your-project/neuroquest:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: Kubernetes Deployment

1. Create namespace:
```bash
kubectl create namespace neuroquest
```

2. Apply configurations:
```bash
kubectl apply -f k8s/ -n neuroquest
```

3. Check deployment:
```bash
kubectl get pods -n neuroquest
kubectl get services -n neuroquest
```

## SSL/TLS Configuration

### Using Let's Encrypt with Nginx

1. Install Certbot:
```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

2. Generate certificates:
```bash
sudo certbot --nginx -d neuroquest.com -d www.neuroquest.com
```

3. Update nginx.conf:
```nginx
server {
    listen 443 ssl http2;
    server_name neuroquest.com;
    
    ssl_certificate /etc/letsencrypt/live/neuroquest.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/neuroquest.com/privkey.pem;
    
    location / {
        proxy_pass http://app:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Monitoring Setup

### 1. Configure Alerts

Create `prometheus/alerts/app.yml`:

```yaml
groups:
  - name: neuroquest
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: High error rate detected
          
      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, http_request_duration_ms_bucket) > 1000
        for: 10m
        annotations:
          summary: Response time is slow
```

### 2. Setup Grafana Dashboards

Import dashboards:
```bash
# Dashboards are auto-provisioned from grafana/provisioning/dashboards/
docker-compose restart grafana
```

### 3. Configure Sentry

1. Create project in Sentry
2. Add DSN to environment variables
3. Configure alerts in Sentry dashboard

## Database Migrations

Run migrations before deployment:

```bash
# Local machine
npx prisma migrate deploy

# Or in Docker
docker-compose exec app npx prisma migrate deploy
```

## Performance Optimization

### 1. Enable Caching

Update `next.config.js`:
```javascript
module.exports = {
  headers: async () => [
    {
      source: '/_next/static/(.*)',
      headers: [
        {
          key: 'Cache-Control',
          value: 'public, max-age=31536000, immutable',
        },
      ],
    },
  ],
}
```

### 2. CDN Configuration

For Cloudflare:
1. Add domain to Cloudflare
2. Enable proxy (orange cloud)
3. Configure page rules:
   - Cache Level: Cache Everything
   - Edge Cache TTL: 1 month

### 3. Image Optimization

Use Next.js Image component and configure domains:
```javascript
module.exports = {
  images: {
    domains: ['your-cdn.com'],
  },
}
```

## Health Checks

### Application Health

```bash
# Check app health
curl http://localhost:3000/api/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "up",
    "api": "up"
  }
}
```

### Container Health

```bash
# Check all containers
docker-compose ps

# Check specific service
docker-compose exec app sh -c "ps aux"
```

## Backup Strategy

### Database Backup

```bash
# Manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Automated daily backup (cron)
0 2 * * * pg_dump $DATABASE_URL > /backups/db_$(date +\%Y\%m\%d).sql
```

### Application Backup

```bash
# Backup volumes
docker run --rm -v neuroquest_app-data:/data -v $(pwd):/backup alpine tar czf /backup/app-backup.tar.gz /data
```

## Rollback Procedure

If deployment fails:

1. **Quick Rollback**:
```bash
# Revert to previous version
docker-compose down
git checkout previous-tag
docker-compose up -d --build
```

2. **Database Rollback**:
```bash
# Restore from backup
psql $DATABASE_URL < backup_20240115.sql
```

3. **Feature Flag Disable**:
```javascript
// Disable problematic feature
if (process.env.FEATURE_FLAG_NEW_FEATURE !== 'true') {
  return <OldFeature />
}
```

## Security Checklist

- [ ] Environment variables secured
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Security headers set
- [ ] Database connections encrypted
- [ ] Secrets rotated regularly
- [ ] Monitoring alerts configured
- [ ] Backup strategy implemented
- [ ] DDoS protection enabled

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs neuroquest-app

# Inspect container
docker inspect neuroquest-app

# Check resources
docker system df
```

### Database connection issues
```bash
# Test connection
docker-compose exec app npx prisma db pull

# Check network
docker network ls
docker network inspect neuroquest_neuroquest-network
```

### High memory usage
```bash
# Check memory
docker stats

# Limit memory in docker-compose.yml
services:
  app:
    mem_limit: 1g
```

## Maintenance Mode

Enable maintenance mode:

```bash
# Create maintenance page
echo "Under maintenance" > public/maintenance.html

# Update nginx to serve maintenance page
location / {
    if (-f $document_root/maintenance.html) {
        return 503;
    }
    proxy_pass http://app:3000;
}

error_page 503 @maintenance;
location @maintenance {
    root /usr/share/nginx/html;
    rewrite ^.*$ /maintenance.html break;
}
```

## Support

For deployment issues:
1. Check deployment logs
2. Review monitoring dashboards
3. Check GitHub Actions for CI/CD status
4. Contact support with error details