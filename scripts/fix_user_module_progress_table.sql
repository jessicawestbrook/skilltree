-- Fix user_module_progress table by adding missing columns

-- Add status column if it doesn't exist
ALTER TABLE user_module_progress 
ADD COLUMN IF NOT EXISTS status VARCHAR(50) 
DEFAULT 'not_started' 
CHECK (status IN ('not_started', 'in_progress', 'completed'));

-- Add updated_at column if it doesn't exist
ALTER TABLE user_module_progress 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- Add last_accessed column to track when user last viewed/worked on the module
ALTER TABLE user_module_progress 
ADD COLUMN IF NOT EXISTS last_accessed TIMESTAMPTZ DEFAULT NOW();

-- Create an update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the trigger to user_module_progress table
DROP TRIGGER IF EXISTS update_user_module_progress_updated_at ON user_module_progress;
CREATE TRIGGER update_user_module_progress_updated_at 
BEFORE UPDATE ON user_module_progress 
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_module_progress_status ON user_module_progress(status);
CREATE INDEX IF NOT EXISTS idx_user_module_progress_updated_at ON user_module_progress(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_module_progress_last_accessed ON user_module_progress(last_accessed DESC);

-- Verify the columns were added
SELECT 
    column_name, 
    data_type, 
    column_default,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'user_module_progress'
ORDER BY ordinal_position;

-- Show success message
SELECT 'SUCCESS: user_module_progress table has been fixed with status and updated_at columns' as message;