import { PrismaClient } from '@prisma/client';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as crypto from 'crypto';

const prisma = new PrismaClient();

interface MigrationFile {
  version: string;
  name: string;
  path: string;
  checksum: string;
}

interface MigrationConfig {
  dryRun?: boolean;
  target?: string;
  rollback?: boolean;
}

class MigrationRunner {
  private migrationsDir: string;

  constructor(migrationsDir: string = './prisma/migrations/sql') {
    this.migrationsDir = migrationsDir;
  }

  /**
   * Calculate checksum for a migration file
   */
  private async calculateChecksum(filePath: string): Promise<string> {
    const content = await fs.readFile(filePath, 'utf-8');
    return crypto.createHash('sha256').update(content).digest('hex');
  }

  /**
   * Get all migration files from the migrations directory
   */
  private async getMigrationFiles(): Promise<MigrationFile[]> {
    const files = await fs.readdir(this.migrationsDir);
    const migrations: MigrationFile[] = [];

    for (const file of files) {
      if (!file.endsWith('.sql')) continue;

      const match = file.match(/^(\d{4})_(.+)\.sql$/);
      if (!match) continue;

      const filePath = path.join(this.migrationsDir, file);
      const checksum = await this.calculateChecksum(filePath);

      migrations.push({
        version: match[1],
        name: match[2],
        path: filePath,
        checksum
      });
    }

    return migrations.sort((a, b) => a.version.localeCompare(b.version));
  }

  /**
   * Get applied migrations from the database
   */
  private async getAppliedMigrations(): Promise<any[]> {
    return await prisma.$queryRaw`
      SELECT version, name, checksum, applied_at, success
      FROM migrations
      WHERE rolled_back_at IS NULL
      ORDER BY version
    `;
  }

  /**
   * Apply a single migration
   */
  private async applyMigration(migration: MigrationFile, dryRun: boolean = false) {
    const startTime = Date.now();
    console.log(`\n📦 Applying migration ${migration.version}: ${migration.name}`);

    if (dryRun) {
      console.log('  ✅ [DRY RUN] Would apply migration');
      return;
    }

    const sql = await fs.readFile(migration.path, 'utf-8');
    
    // Start transaction
    try {
      await prisma.$transaction(async (tx: any) => {
        // Execute migration SQL
        await tx.$executeRawUnsafe(sql);

        // Record migration
        await tx.$executeRaw`
          INSERT INTO migrations (version, name, checksum, execution_time, success)
          VALUES (${migration.version}, ${migration.name}, ${migration.checksum}, 
                  ${Date.now() - startTime}, true)
        `;
      });

      console.log(`  ✅ Migration applied successfully (${Date.now() - startTime}ms)`);
    } catch (error) {
      console.error(`  ❌ Migration failed: ${error}`);
      
      // Record failed migration
      await prisma.$executeRaw`
        INSERT INTO migrations (version, name, checksum, execution_time, success, error)
        VALUES (${migration.version}, ${migration.name}, ${migration.checksum}, 
                ${Date.now() - startTime}, false, ${String(error)})
      `;
      
      throw error;
    }
  }

  /**
   * Rollback a migration
   */
  private async rollbackMigration(version: string) {
    console.log(`\n🔄 Rolling back migration ${version}`);
    
    const rollbackPath = path.join(this.migrationsDir, 'rollback', `${version}_rollback.sql`);
    
    try {
      const rollbackSql = await fs.readFile(rollbackPath, 'utf-8');
      
      await prisma.$transaction(async (tx: any) => {
        // Execute rollback SQL
        await tx.$executeRawUnsafe(rollbackSql);

        // Mark migration as rolled back
        await tx.$executeRaw`
          UPDATE migrations 
          SET rolled_back_at = NOW()
          WHERE version = ${version}
        `;
      });

      console.log(`  ✅ Rollback completed successfully`);
    } catch (error) {
      if ((error as NodeJS.ErrnoException)?.code === 'ENOENT') {
        console.error(`  ❌ No rollback script found for migration ${version}`);
      } else {
        console.error(`  ❌ Rollback failed: ${error}`);
      }
      throw error;
    }
  }

  /**
   * Run migrations
   */
  async run(config: MigrationConfig = {}) {
    console.log('🚀 Starting migration runner...\n');

    try {
      // Ensure migrations table exists
      await this.ensureMigrationsTable();

      const migrations = await this.getMigrationFiles();
      const applied = await this.getAppliedMigrations();

      if (config.rollback && config.target) {
        // Rollback to specific version
        const toRollback = applied
          .filter((m) => m.version > config.target!)
          .reverse();

        for (const migration of toRollback) {
          await this.rollbackMigration(migration.version);
        }
        return;
      }

      // Find pending migrations
      const appliedVersions = new Set(applied.map((m) => m.version));
      const pending = migrations.filter(m => !appliedVersions.has(m.version));

      if (pending.length === 0) {
        console.log('✨ No pending migrations');
        return;
      }

      console.log(`Found ${pending.length} pending migration(s)`);

      // Apply migrations up to target
      for (const migration of pending) {
        if (config.target && migration.version > config.target) {
          console.log(`Stopping at target version ${config.target}`);
          break;
        }

        // Check for checksum mismatch
        const existing = applied.find((m) => m.version === migration.version);
        if (existing && existing.checksum !== migration.checksum) {
          throw new Error(
            `Checksum mismatch for migration ${migration.version}. ` +
            `Database has ${existing.checksum}, file has ${migration.checksum}`
          );
        }

        await this.applyMigration(migration, config.dryRun);
      }

      console.log('\n✅ All migrations completed successfully');
    } catch (error) {
      console.error('\n❌ Migration failed:', error);
      process.exit(1);
    } finally {
      await prisma.$disconnect();
    }
  }

  /**
   * Ensure migrations tracking table exists
   */
  private async ensureMigrationsTable() {
    await prisma.$executeRaw`
      CREATE TABLE IF NOT EXISTS migrations (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        version VARCHAR(10) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        checksum VARCHAR(64),
        execution_time INTEGER,
        success BOOLEAN DEFAULT true,
        error TEXT,
        rolled_back_at TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      )
    `;

    await prisma.$executeRaw`
      CREATE INDEX IF NOT EXISTS idx_migrations_version ON migrations(version);
    `;

    await prisma.$executeRaw`
      CREATE INDEX IF NOT EXISTS idx_migrations_applied_at ON migrations(applied_at);
    `;
  }

  /**
   * Generate a new migration file
   */
  async generate(name: string) {
    const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const version = String(Date.now()).slice(-4);
    const filename = `${version}_${name}.sql`;
    const filepath = path.join(this.migrationsDir, filename);
    
    const template = `-- Migration: ${name}
-- Version: ${version}
-- Date: ${new Date().toISOString()}

-- ============================================
-- UP MIGRATION
-- ============================================

-- Add your migration SQL here


-- ============================================
-- Add rollback script in rollback/${version}_rollback.sql
-- ============================================
`;

    await fs.writeFile(filepath, template);
    console.log(`✅ Created migration: ${filename}`);
    
    // Create rollback template
    const rollbackPath = path.join(this.migrationsDir, 'rollback', `${version}_rollback.sql`);
    const rollbackTemplate = `-- Rollback for migration: ${name}
-- Version: ${version}

-- Add your rollback SQL here
`;
    
    await fs.mkdir(path.dirname(rollbackPath), { recursive: true });
    await fs.writeFile(rollbackPath, rollbackTemplate);
    console.log(`✅ Created rollback template: rollback/${version}_rollback.sql`);
  }

  /**
   * Show migration status
   */
  async status() {
    await this.ensureMigrationsTable();
    
    const migrations = await this.getMigrationFiles();
    const applied = await this.getAppliedMigrations();
    const appliedMap = new Map(applied.map((m) => [m.version, m]));

    console.log('\n📊 Migration Status\n');
    console.log('Version | Status    | Name');
    console.log('--------|-----------|---------------------');

    for (const migration of migrations) {
      const appliedMigration = appliedMap.get(migration.version);
      let status = '⏳ Pending';
      
      if (appliedMigration) {
        if (appliedMigration.rolled_back_at) {
          status = '🔄 Rolled back';
        } else if (appliedMigration.success) {
          status = '✅ Applied';
        } else {
          status = '❌ Failed';
        }
      }

      console.log(`${migration.version}  | ${status} | ${migration.name}`);
    }
  }
}

// CLI interface
if (require.main === module) {
  const command = process.argv[2];
  const runner = new MigrationRunner();

  switch (command) {
    case 'up':
      runner.run({
        target: process.argv[3],
        dryRun: process.argv.includes('--dry-run')
      });
      break;
      
    case 'down':
      runner.run({
        rollback: true,
        target: process.argv[3]
      });
      break;
      
    case 'generate':
      const name = process.argv[3];
      if (!name) {
        console.error('Please provide a migration name');
        process.exit(1);
      }
      runner.generate(name);
      break;
      
    case 'status':
      runner.status();
      break;
      
    default:
      console.log(`
Database Migration Runner

Commands:
  up [target]        Run pending migrations up to target version
  down <target>      Rollback migrations down to target version  
  generate <name>    Generate a new migration file
  status            Show migration status

Options:
  --dry-run         Show what would be done without applying changes

Examples:
  npm run migrate:up
  npm run migrate:up 0004
  npm run migrate:down 0002
  npm run migrate:generate add_user_preferences
  npm run migrate:status
      `);
  }
}

export default MigrationRunner;