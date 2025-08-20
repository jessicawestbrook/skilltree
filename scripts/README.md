# Claude API Scripts

This directory contains Python scripts for interacting with the Claude API.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Anthropic API key as an environment variable:
```bash
# Windows
set ANTHROPIC_API_KEY=your_api_key_here

# Linux/Mac
export ANTHROPIC_API_KEY=your_api_key_here
```

## Scripts

### claude_api_example.py
A comprehensive example script that demonstrates how to:
- Make basic API calls to Claude
- Generate example sentences for vocabulary words
- Get concept explanations
- Run in interactive mode

**Usage:**
```bash
python claude_api_example.py
```

**Features:**
- Simple question answering
- Educational content generation
- Interactive chat mode
- Error handling and validation

## API Key Setup

You can get your API key from the [Anthropic Console](https://console.anthropic.com/). The key should start with `sk-ant-`.

Make sure to keep your API key secure and never commit it to version control.