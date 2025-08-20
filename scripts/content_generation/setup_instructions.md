# Setup Instructions for Learning Content Generator

## Quick Start Guide

### 1. Get Your Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it will start with `sk-ant-`)

### 2. Set Environment Variables

You need to set three environment variables:

**Option A: Using Command Line**

Windows:
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-api-key-here
set REACT_APP_SUPABASE_URL=https://your-project.supabase.co
set REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
```

macOS/Linux:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-api-key-here
export REACT_APP_SUPABASE_URL=https://your-project.supabase.co
export REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
```

**Option B: Create .env file**

Create a `.env` file in your project root:
```
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### 3. Install Dependencies

```bash
cd scripts/content_generation
pip install -r requirements.txt
```

### 4. Test the Setup

```bash
python test_generator.py
```

This will test all connections and functionality before processing real data.

### 5. Run Content Generation

**Start small for testing:**
```bash
python learning_content_generator.py --max-nodes 1
```

**Get cost estimate:**
```bash
python learning_content_generator.py --estimate-only
```

**Full processing:**
```bash
python learning_content_generator.py
```

## Cost Information

- Estimated cost: ~$0.50-0.75 per skill tree node
- For 100 nodes: approximately $50-75 USD
- For 1000 nodes: approximately $500-750 USD

Always run `--estimate-only` first to get accurate costs for your specific data.

## Support

If you encounter issues:
1. Run the test script: `python test_generator.py`
2. Check that all environment variables are set correctly
3. Verify your Anthropic API key has sufficient credits
4. Ensure your Supabase database has the required tables