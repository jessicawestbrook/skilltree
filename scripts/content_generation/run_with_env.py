#!/usr/bin/env python3
"""
Environment loader script for the learning content generator.
This script loads environment variables from the project .env.local file.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env.local
env_file = project_root / '.env.local'
if env_file.exists():
    print(f"Loading environment from: {env_file}")
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    print("Environment variables loaded successfully")
else:
    print(f"Warning: .env.local file not found at {env_file}")

# Now run the content generator
if __name__ == "__main__":
    from learning_content_generator import main
    main()