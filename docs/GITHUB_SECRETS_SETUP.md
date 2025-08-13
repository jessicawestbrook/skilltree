# GitHub Secrets Setup Guide

This guide explains how to configure GitHub Secrets for the NeuroQuest CI/CD pipeline.

## Required Secrets

Navigate to your GitHub repository → Settings → Secrets and variables → Actions, then add the following secrets:

### 1. Supabase Configuration

#### `NEXT_PUBLIC_SUPABASE_URL`
- **Value**: Your Supabase project URL
- **Example**: `https://bedcscnprmaztktgklko.supabase.co`
- **How to find**: Supabase Dashboard → Settings → API → Project URL

#### `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Value**: Your Supabase anonymous/public key
- **Example**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **How to find**: Supabase Dashboard → Settings → API → Project API keys → anon/public

#### `SUPABASE_SERVICE_ROLE_KEY`
- **Value**: Your Supabase service role key (keep this secret!)
- **Example**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **How to find**: Supabase Dashboard → Settings → API → Project API keys → service_role

#### `DATABASE_URL`
- **Value**: PostgreSQL connection string
- **Format**: `postgresql://[user]:[password]@[host]:[port]/[database]`
- **Example**: `postgresql://postgres:password@db.supabase.co:5432/postgres`
- **How to find**: Supabase Dashboard → Settings → Database → Connection string

### 2. Push Notifications (Web Push)

#### `NEXT_PUBLIC_VAPID_PUBLIC_KEY`
- **Value**: VAPID public key for web push
- **Current**: `BNkg5Cnp4DKqEwm6eUPq1drv2srpYkzFQPpSXFzRZ8sQgc1TuwuYFhAP5yhJUU21DDgiWopbHaUNsIEvU0LihX8`
- **Generate new**: Run `node scripts/generate-vapid-keys.js`

#### `VAPID_PRIVATE_KEY`
- **Value**: VAPID private key for web push (keep this secret!)
- **Current**: `0Xi0bClIF5TaZRYM8XPX-_0lRciPk9WWXTuRE2PKx2w`
- **Generate new**: Run `node scripts/generate-vapid-keys.js`

### 3. Email Service

#### `RESEND_API_KEY`
- **Value**: Your Resend API key
- **Example**: `re_Nrds1cea_PrTWfYA36sD3qmNbuqurrFhL`
- **How to get**: [Resend Dashboard](https://resend.com/api-keys) → Create API Key

### 4. Monitoring & Analytics (Optional)

#### `SENTRY_DSN`
- **Value**: Sentry Data Source Name
- **Example**: `https://abc123@o123456.ingest.sentry.io/123456`
- **How to get**: Sentry → Project Settings → Client Keys (DSN)

#### `SENTRY_AUTH_TOKEN`
- **Value**: Sentry authentication token for source maps
- **How to get**: Sentry → Settings → Auth Tokens → Create New Token

#### `CODECOV_TOKEN`
- **Value**: Codecov upload token
- **How to get**: [Codecov](https://codecov.io) → Repository Settings → Upload Token

#### `LHCI_GITHUB_APP_TOKEN`
- **Value**: Lighthouse CI GitHub App token
- **How to get**: [Lighthouse CI GitHub App](https://github.com/apps/lighthouse-ci)

### 5. Container Registry (For Docker deployment)

#### `DOCKER_USERNAME`
- **Value**: Docker Hub username
- **Example**: `yourusername`

#### `DOCKER_PASSWORD`
- **Value**: Docker Hub password or access token
- **Recommended**: Use access token instead of password
- **How to get**: Docker Hub → Account Settings → Security → Access Tokens

### 6. Deployment Secrets (For production)

#### `GRAFANA_USER`
- **Value**: Grafana admin username
- **Default**: `admin`

#### `GRAFANA_PASSWORD`
- **Value**: Grafana admin password
- **Recommendation**: Use strong password

#### `REDIS_URL`
- **Value**: Redis connection URL (if using external Redis)
- **Format**: `redis://[password]@[host]:[port]`
- **Local Docker**: `redis://redis:6379`

## How to Add Secrets

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter the secret name (e.g., `NEXT_PUBLIC_SUPABASE_URL`)
6. Enter the secret value
7. Click **Add secret**

## Security Best Practices

1. **Never commit secrets to your repository**
   - Use `.env.local` for local development
   - Add `.env.local` to `.gitignore`

2. **Rotate secrets regularly**
   - Update VAPID keys every 6 months
   - Rotate API keys annually
   - Change service role keys if compromised

3. **Use least privilege principle**
   - Create API keys with minimal required permissions
   - Use different keys for different environments

4. **Monitor secret usage**
   - Check GitHub Actions logs for unauthorized access
   - Monitor API key usage in respective dashboards

## Verifying Your Setup

After adding all secrets, trigger a CI/CD run to verify:

```bash
# Push to main branch
git push origin main

# Or manually trigger workflow
gh workflow run ci.yml
```

Check the Actions tab in your GitHub repository to see if the workflow runs successfully.

## Environment-Specific Secrets

For multiple environments (staging, production), use environment-specific secrets:

- `STAGING_SUPABASE_URL`
- `PRODUCTION_SUPABASE_URL`

And reference them in your workflow:

```yaml
env:
  NEXT_PUBLIC_SUPABASE_URL: ${{ secrets[format('{0}_SUPABASE_URL', env.ENVIRONMENT)] }}
```

## Troubleshooting

### Build fails with "Missing environment variable"
- Ensure all required secrets are added
- Check secret names match exactly (case-sensitive)
- Verify no typos in workflow file

### "Invalid VAPID key" error
- Regenerate VAPID keys using the script
- Ensure keys are base64 encoded properly
- Check both public and private keys are set

### Database connection issues
- Verify DATABASE_URL format is correct
- Check network access rules in Supabase
- Ensure SSL mode is configured if required

## Support

For issues with secrets setup:
1. Check GitHub Actions logs for specific errors
2. Verify secret values in respective service dashboards
3. Open an issue in the repository with error details (without exposing secrets)