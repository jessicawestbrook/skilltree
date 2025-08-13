# 🗄️ Database Migration Strategy

## Overview
This document outlines the comprehensive database migration strategy for NeuroQuest using Prisma ORM with custom migration runner and rollback procedures.

## Table of Contents
- [Architecture](#architecture)
- [Migration System](#migration-system)
- [Rollback Procedures](#rollback-procedures)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Architecture

### Technology Stack
- **ORM**: Prisma (Schema-first approach)
- **Database**: PostgreSQL (Supabase)
- **Migration Runner**: Custom TypeScript solution
- **Version Control**: Semantic versioning with checksums

### Directory Structure
```
prisma/
├── schema.prisma              # Prisma schema definition
├── migrations/
│   ├── migration-runner.ts    # Custom migration runner
│   ├── sql/                   # Forward migration scripts
│   │   ├── 0001_initial_schema.sql
│   │   ├── 0002_user_tables.sql
│   │   └── ...
│   └── rollback/              # Rollback scripts
│       ├── 0001_rollback.sql
│       ├── 0002_rollback.sql
│       └── ...
```

## Migration System

### 1. Prisma Schema Management

The Prisma schema (`prisma/schema.prisma`) defines the complete database structure:

```prisma
model KnowledgeNode {
  id          String   @id @default(uuid())
  name        String
  // ... other fields
  
  @@map("knowledge_nodes") // Maps to existing table
}
```

### 2. Migration Workflow

#### Creating a New Migration

```bash
# Generate migration files
npm run db:migrate:generate add_feature_name

# This creates:
# - prisma/migrations/sql/XXXX_add_feature_name.sql
# - prisma/migrations/rollback/XXXX_rollback.sql
```

#### Migration File Template

```sql
-- Migration: add_user_preferences
-- Version: 0002
-- Date: 2024-01-15

-- UP MIGRATION
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  theme VARCHAR(20) DEFAULT 'light'
);

CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
```

#### Rollback File Template

```sql
-- Rollback for: add_user_preferences
-- Version: 0002

DROP INDEX IF EXISTS idx_user_preferences_user_id;
DROP TABLE IF EXISTS user_preferences CASCADE;
```

### 3. Running Migrations

#### Development Environment

```bash
# Check migration status
npm run db:migrate:status

# Run all pending migrations
npm run db:migrate:up

# Run up to specific version
npm run db:migrate:up 0005

# Dry run (preview changes)
npm run db:migrate:up -- --dry-run
```

#### Production Environment

```bash
# Deploy migrations with Prisma
npm run prisma:migrate:deploy

# Or use custom runner with safety checks
NODE_ENV=production npm run db:migrate:up
```

### 4. Migration Tracking

Migrations are tracked in the `migrations` table:

```sql
CREATE TABLE migrations (
  id UUID PRIMARY KEY,
  version VARCHAR(10) UNIQUE,
  name VARCHAR(255),
  checksum VARCHAR(64),
  applied_at TIMESTAMP,
  execution_time INTEGER,
  success BOOLEAN,
  error TEXT,
  rolled_back_at TIMESTAMP
);
```

## Rollback Procedures

### Automatic Rollback

The migration runner supports automatic rollback on failure:

```typescript
// Migration runner automatically creates savepoint
await prisma.$transaction(async (tx) => {
  await tx.$executeRawUnsafe(migrationSql);
  // If this fails, automatic rollback occurs
});
```

### Manual Rollback

```bash
# Rollback to specific version
npm run db:migrate:down 0003

# This will:
# 1. Execute rollback scripts for versions > 0003
# 2. Update migration tracking table
# 3. Verify database state
```

### Rollback Strategy

1. **Immediate Rollback**: For failed migrations
2. **Staged Rollback**: For production issues
3. **Point-in-Time Recovery**: Using database backups

### Creating Safe Rollbacks

```sql
-- Safe rollback example
BEGIN;

-- Save current data if needed
CREATE TABLE user_preferences_backup AS 
SELECT * FROM user_preferences;

-- Perform rollback
DROP TABLE user_preferences CASCADE;

-- Verify rollback
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables 
             WHERE table_name = 'user_preferences') THEN
    RAISE EXCEPTION 'Rollback failed: table still exists';
  END IF;
END $$;

COMMIT;
```

## Best Practices

### 1. Migration Guidelines

- **Atomic Operations**: Each migration should be self-contained
- **Idempotent Scripts**: Migrations should be safe to run multiple times
- **Data Preservation**: Always backup data before destructive changes
- **Testing**: Test migrations on staging before production

### 2. Schema Evolution Patterns

#### Adding Columns
```sql
-- Safe: Add nullable column
ALTER TABLE users ADD COLUMN preferences JSONB;

-- Then add constraints in separate migration
ALTER TABLE users ALTER COLUMN preferences SET NOT NULL;
```

#### Renaming Columns
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Step 2: Copy data
UPDATE users SET email_address = email;

-- Step 3: Drop old column (in next migration)
ALTER TABLE users DROP COLUMN email;
```

#### Creating Indexes
```sql
-- Create index concurrently to avoid locks
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### 3. Version Control Integration

```bash
# Pre-commit hook (.git/hooks/pre-commit)
#!/bin/bash

# Validate Prisma schema
npx prisma format
npx prisma validate

# Check for migration conflicts
npm run db:migrate:status
```

### 4. CI/CD Pipeline

```yaml
# .github/workflows/migrations.yml
name: Database Migrations

on:
  pull_request:
    paths:
      - 'prisma/**'
      - 'scripts/**.sql'

jobs:
  test-migrations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup test database
        run: docker-compose up -d postgres
      
      - name: Run migrations
        run: npm run db:migrate:up -- --dry-run
      
      - name: Test rollbacks
        run: npm run db:migrate:down 0001 -- --dry-run
```

## Advanced Features

### 1. Blue-Green Deployments

```sql
-- Create new version alongside old
CREATE TABLE users_v2 AS SELECT * FROM users;

-- Add new columns
ALTER TABLE users_v2 ADD COLUMN new_feature JSONB;

-- Switch in transaction
BEGIN;
ALTER TABLE users RENAME TO users_old;
ALTER TABLE users_v2 RENAME TO users;
COMMIT;
```

### 2. Zero-Downtime Migrations

```typescript
// Progressive migration
class ProgressiveMigration {
  async migrate(batchSize: number = 1000) {
    let offset = 0;
    let hasMore = true;
    
    while (hasMore) {
      const batch = await prisma.$queryRaw`
        UPDATE users 
        SET migrated = true 
        WHERE id IN (
          SELECT id FROM users 
          WHERE migrated = false 
          LIMIT ${batchSize}
        )
        RETURNING id
      `;
      
      hasMore = batch.length === batchSize;
      offset += batchSize;
      
      // Pause to reduce load
      await new Promise(r => setTimeout(r, 100));
    }
  }
}
```

### 3. Data Migration Patterns

```typescript
// Data transformation during migration
async function migrateUserData() {
  const users = await prisma.user.findMany();
  
  for (const user of users) {
    await prisma.userProfile.create({
      data: {
        userId: user.id,
        displayName: user.name || user.email.split('@')[0],
        // Transform old data to new format
        preferences: {
          theme: user.darkMode ? 'dark' : 'light',
          notifications: user.emailNotifications
        }
      }
    });
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Migration Checksum Mismatch
```bash
# Error: Checksum mismatch for migration 0003
# Solution: Verify file hasn't been modified
git diff prisma/migrations/sql/0003_add_feature.sql

# If intentional, update checksum in database
UPDATE migrations SET checksum = 'new_checksum' WHERE version = '0003';
```

#### 2. Failed Migration Recovery
```bash
# Check migration status
npm run db:migrate:status

# Mark migration as rolled back
UPDATE migrations SET rolled_back_at = NOW() WHERE version = '0004';

# Re-run migration
npm run db:migrate:up 0004
```

#### 3. Lock Conflicts
```sql
-- Check for locks
SELECT * FROM pg_locks WHERE NOT granted;

-- Kill blocking queries
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle in transaction' 
  AND query_start < NOW() - INTERVAL '5 minutes';
```

### Monitoring

```sql
-- Migration health check
CREATE VIEW migration_health AS
SELECT 
  version,
  name,
  applied_at,
  execution_time,
  CASE 
    WHEN rolled_back_at IS NOT NULL THEN 'rolled_back'
    WHEN success = false THEN 'failed'
    ELSE 'applied'
  END as status
FROM migrations
ORDER BY version DESC
LIMIT 10;
```

## Emergency Procedures

### Database Backup Before Migration
```bash
# Create backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Verify backup
pg_restore --list backup_*.sql
```

### Emergency Rollback
```bash
# Stop application
kubectl scale deployment neuroquest --replicas=0

# Rollback database
npm run db:migrate:down $LAST_GOOD_VERSION

# Restore from backup if needed
psql $DATABASE_URL < backup_20240115_120000.sql

# Restart application with previous version
kubectl set image deployment/neuroquest app=neuroquest:$PREVIOUS_VERSION
kubectl scale deployment neuroquest --replicas=3
```

## Migration Checklist

- [ ] Schema changes reviewed by team
- [ ] Migration script tested locally
- [ ] Rollback script created and tested
- [ ] Data backup strategy confirmed
- [ ] Performance impact assessed
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [ ] Stakeholders notified

## Resources

- [Prisma Migration Guide](https://www.prisma.io/docs/concepts/components/prisma-migrate)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don't_Do_This)
- [Zero-Downtime Migrations](https://github.com/ankane/strong_migrations)

---

Last Updated: January 2024
Version: 1.0.0