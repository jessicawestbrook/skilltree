#!/usr/bin/env python3
"""
Generate ALL Level 2 & 3 Node Descriptions (Overwrite Mode)
===========================================================

This script generates descriptions for ALL second and third level nodes in the skill tree,
overwriting any existing descriptions to ensure consistency with the improved approach.

Level 2: Main Categories (74 nodes total)  
Level 3: Subcategories (374 nodes total)
Total: 448 nodes to process

Features:
- Processes ALL nodes regardless of existing descriptions
- Automatic checkpoint saving every 10 nodes
- Resume from interruption
- Progress tracking with ETA
- Error handling and retry logic
- Cost and time tracking
- Detailed logging

Usage:
    python generate_all_level2_level3_descriptions.py --batch-size 20
    python generate_all_level2_level3_descriptions.py --resume
    python generate_all_level2_level3_descriptions.py --dry-run --limit 10
"""

import os
import sys
import argparse
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enhanced_content_generator import EnhancedContentGenerator, SkillTreeNode

# Load environment variables
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env.local'))
except ImportError:
    print("Warning: python-dotenv not available. Please ensure environment variables are set manually.")

class AllLevel23ProgressTracker:
    """Enhanced progress tracker for ALL Level 2 & 3 description generation."""
    
    def __init__(self, checkpoint_file='all_level2_level3_progress.json'):
        self.checkpoint_file = checkpoint_file
        self.start_time = datetime.now()
        self.session_start = datetime.now()
        
        # Progress counters
        self.total_processed = 0
        self.level2_processed = 0
        self.level3_processed = 0
        self.successful = 0
        self.failed = 0
        
        # Tracking
        self.processed_ids = set()
        self.failed_nodes = []
        self.level2_stats = {'total': 0, 'processed': 0, 'successful': 0}
        self.level3_stats = {'total': 0, 'processed': 0, 'successful': 0}
        
        # Cost tracking
        self.api_calls = 0
        self.estimated_cost = 0.0
        
    def load_checkpoint(self) -> bool:
        """Load progress from checkpoint file."""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.total_processed = data.get('total_processed', 0)
                self.level2_processed = data.get('level2_processed', 0)
                self.level3_processed = data.get('level3_processed', 0)
                self.successful = data.get('successful', 0)
                self.failed = data.get('failed', 0)
                self.processed_ids = set(data.get('processed_ids', []))
                self.failed_nodes = data.get('failed_nodes', [])
                self.level2_stats = data.get('level2_stats', {'total': 0, 'processed': 0, 'successful': 0})
                self.level3_stats = data.get('level3_stats', {'total': 0, 'processed': 0, 'successful': 0})
                self.api_calls = data.get('api_calls', 0)
                self.estimated_cost = data.get('estimated_cost', 0.0)
                
                if data.get('start_time'):
                    self.start_time = datetime.fromisoformat(data['start_time'])
                
                print(f"Resuming from checkpoint:")
                print(f"   Total processed: {self.total_processed}")
                print(f"   Level 2: {self.level2_processed}, Level 3: {self.level3_processed}")
                print(f"   Successful: {self.successful}, Failed: {self.failed}")
                print()
                
                return True
                
            except Exception as e:
                print(f"[ERROR] Error loading checkpoint: {e}")
                return False
        
        return False
    
    def save_checkpoint(self):
        """Save current progress to checkpoint file."""
        try:
            data = {
                'total_processed': self.total_processed,
                'level2_processed': self.level2_processed,
                'level3_processed': self.level3_processed,
                'successful': self.successful,
                'failed': self.failed,
                'processed_ids': list(self.processed_ids),
                'failed_nodes': self.failed_nodes,
                'level2_stats': self.level2_stats,
                'level3_stats': self.level3_stats,
                'api_calls': self.api_calls,
                'estimated_cost': self.estimated_cost,
                'start_time': self.start_time.isoformat(),
                'last_save': datetime.now().isoformat()
            }
            
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"[WARNING]  Error saving checkpoint: {e}")
    
    def record_success(self, node: SkillTreeNode, level: int):
        """Record successful description generation."""
        self.total_processed += 1
        self.successful += 1
        self.api_calls += 1
        self.estimated_cost += 0.02
        self.processed_ids.add(node.id)
        
        if level == 2:
            self.level2_processed += 1
            self.level2_stats['processed'] += 1
            self.level2_stats['successful'] += 1
        elif level == 3:
            self.level3_processed += 1
            self.level3_stats['processed'] += 1
            self.level3_stats['successful'] += 1
        
        # Save checkpoint every 10 successful operations
        if self.successful % 10 == 0:
            self.save_checkpoint()
    
    def record_failure(self, node: SkillTreeNode, level: int, error: str):
        """Record failed description generation."""
        self.total_processed += 1
        self.failed += 1
        self.processed_ids.add(node.id)
        
        if level == 2:
            self.level2_processed += 1
            self.level2_stats['processed'] += 1
        elif level == 3:
            self.level3_processed += 1
            self.level3_stats['processed'] += 1
        
        self.failed_nodes.append({
            'id': node.id,
            'name': node.name,
            'level': level,
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        })
        
        self.save_checkpoint()
    
    def print_progress(self, current_total: int, target_total: int):
        """Print detailed progress report."""
        elapsed = datetime.now() - self.start_time
        session_elapsed = datetime.now() - self.session_start
        
        if self.total_processed > 0:
            rate = self.total_processed / elapsed.total_seconds() * 60  # per minute
            remaining = target_total - current_total
            eta_minutes = remaining / rate if rate > 0 else 0
            eta = datetime.now() + timedelta(minutes=eta_minutes)
        else:
            eta = None
            rate = 0
        
        print(f"\n[PROGRESS] PROGRESS REPORT")
        print(f"==================")
        print(f"Overall: {current_total}/{target_total} ({(current_total/target_total*100):.1f}%)")
        print(f"Level 2: {self.level2_processed} processed ({self.level2_stats['successful']} successful)")
        print(f"Level 3: {self.level3_processed} processed ({self.level3_stats['successful']} successful)")
        print(f"Success rate: {(self.successful/max(1,self.total_processed)*100):.1f}%")
        print(f"Processing rate: {rate:.1f} nodes/minute")
        print(f"Session time: {session_elapsed}")
        print(f"Total time: {elapsed}")
        if eta:
            print(f"ETA: {eta.strftime('%H:%M:%S')}")
        print(f"Estimated cost so far: ${self.estimated_cost:.2f}")
        
        if self.failed > 0:
            print(f"[WARNING]  Recent failures: {len([f for f in self.failed_nodes if f['timestamp'] > (datetime.now() - timedelta(minutes=30)).isoformat()])}")
        
        print()

def get_all_level2_level3_nodes(generator: EnhancedContentGenerator, processed_ids: set) -> Tuple[List[SkillTreeNode], List[SkillTreeNode]]:
    """Get ALL Level 2 and Level 3 nodes (overwriting existing descriptions)."""
    try:
        # Get all nodes with path information
        response = generator.supabase.table('skill_tree_nodes').select('*').order('path').execute()
        
        if not response.data:
            return [], []
        
        level2_nodes = []
        level3_nodes = []
        
        for row in response.data:
            # Skip if already processed in this session
            if row['id'] in processed_ids:
                continue
            
            # NO CHECK FOR EXISTING DESCRIPTIONS - we want to overwrite them
            
            # Check path level
            if row.get('path') and isinstance(row['path'], list):
                level = len(row['path'])
                
                node = SkillTreeNode(
                    id=row['id'],
                    name=row['name'],
                    type='category' if level <= 3 else 'skill',  # Assume upper levels are categories
                    path=row['path'],
                    learning_area=row['learning_area'],
                    has_learning_content=row['has_learning_content'],
                    learning_content_ids=row['learning_content_ids'],
                    is_menu_leaf=row['is_menu_leaf'],
                    description=row.get('description'),
                    parent_id=row['parent_id'],
                    metadata=row['metadata']
                )
                
                if level == 2:
                    level2_nodes.append(node)
                elif level == 3:
                    level3_nodes.append(node)
        
        return level2_nodes, level3_nodes
        
    except Exception as e:
        print(f"[ERROR] Error fetching nodes: {e}")
        return [], []

def generate_description_for_node(generator: EnhancedContentGenerator, node: SkillTreeNode, level: int, dry_run: bool = False) -> bool:
    """Generate description for a single node."""
    try:
        print(f"[PROCESSING] [Level {level}] Processing: {node.name}")
        print(f"   Path: {' > '.join(node.path) if node.path else 'Unknown'}")
        
        if dry_run:
            # Simulate description generation
            time.sleep(1)  # Simulate API call
            print(f"   [SUCCESS] [DRY RUN] Would generate description")
            return True
        
        # Generate description using the enhanced generator
        success = generator.process_single_node(
            node, 
            generate_description=True, 
            generate_content=False
        )
        
        if success:
            print(f"   [SUCCESS] Successfully generated description")
            return True
        else:
            print(f"   [ERROR] Failed to generate description")
            return False
            
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False

def main():
    """Main function for ALL Level 2 & 3 description generation."""
    parser = argparse.ArgumentParser(description='Generate descriptions for ALL Level 2 & 3 nodes (overwrite mode)')
    parser.add_argument('--batch-size', type=int, default=20, help='Nodes to process per batch (default: 20)')
    parser.add_argument('--resume', action='store_true', help='Resume from last checkpoint')
    parser.add_argument('--dry-run', action='store_true', help='Test run without API calls')
    parser.add_argument('--limit', type=int, help='Limit number of nodes to process (for testing)')
    parser.add_argument('--level2-only', action='store_true', help='Process only Level 2 nodes')
    parser.add_argument('--level3-only', action='store_true', help='Process only Level 3 nodes')
    
    args = parser.parse_args()
    
    print("ALL Level 2 & 3 Description Generator (OVERWRITE MODE)")
    print("=" * 60)
    print(f"Batch size: {args.batch_size}")
    print(f"Resume mode: {args.resume}")
    print(f"Dry run: {args.dry_run}")
    print("Mode: OVERWRITE existing descriptions")
    if args.limit:
        print(f"Limit: {args.limit} nodes")
    if args.level2_only:
        print("Focus: Level 2 only")
    elif args.level3_only:
        print("Focus: Level 3 only")
    print()
    
    # Initialize progress tracker
    tracker = AllLevel23ProgressTracker()
    
    if args.resume:
        if not tracker.load_checkpoint():
            print("No checkpoint found, starting fresh.")
    
    try:
        generator = EnhancedContentGenerator()
        
        # Get target nodes
        level2_nodes, level3_nodes = get_all_level2_level3_nodes(generator, tracker.processed_ids)
        
        # Apply filters
        if args.level2_only:
            level3_nodes = []
        elif args.level3_only:
            level2_nodes = []
        
        # Update stats
        tracker.level2_stats['total'] = len(level2_nodes)
        tracker.level3_stats['total'] = len(level3_nodes)
        
        total_nodes = len(level2_nodes) + len(level3_nodes)
        
        if args.limit:
            # Limit total nodes, prioritizing Level 2
            remaining_limit = args.limit
            if len(level2_nodes) > remaining_limit:
                level2_nodes = level2_nodes[:remaining_limit]
                level3_nodes = []
            else:
                remaining_limit -= len(level2_nodes)
                if len(level3_nodes) > remaining_limit:
                    level3_nodes = level3_nodes[:remaining_limit]
            
            total_nodes = len(level2_nodes) + len(level3_nodes)
        
        print(f"[PLAN] PROCESSING PLAN:")
        print(f"   Level 2 nodes: {len(level2_nodes)}")
        print(f"   Level 3 nodes: {len(level3_nodes)}")
        print(f"   Total to process: {total_nodes}")
        print(f"   Mode: OVERWRITE existing descriptions")
        
        if total_nodes == 0:
            print("[SUCCESS] No nodes to process!")
            return
        
        # Calculate estimates
        time_per_node = 1 if args.dry_run else 30  # seconds
        total_time_minutes = (total_nodes * time_per_node) / 60
        cost_per_node = 0 if args.dry_run else 0.02
        total_cost = total_nodes * cost_per_node
        
        print(f"\n[ESTIMATES] ESTIMATES:")
        print(f"   Time: {total_time_minutes:.1f} minutes ({total_time_minutes/60:.1f} hours)")
        print(f"   Cost: ${total_cost:.2f}")
        
        if not args.dry_run and not args.resume:
            confirm = input(f"\n[QUESTION] Process {total_nodes} nodes with improved descriptions? (y/N): ")
            if confirm.lower() != 'y':
                print("[ERROR] Cancelled.")
                return
        
        print(f"\n[START] Starting description generation...")
        if not args.dry_run:
            print("[NOTE] Note: 25-second delays between API calls for rate limiting")
        print()
        
        # Process Level 2 nodes first (more important)
        all_nodes = [(node, 2) for node in level2_nodes] + [(node, 3) for node in level3_nodes]
        
        for i, (node, level) in enumerate(all_nodes):
            current_pos = tracker.total_processed + 1
            
            print(f"\n[{current_pos}/{total_nodes}] Level {level}: {node.name}")
            
            success = generate_description_for_node(generator, node, level, args.dry_run)
            
            if success:
                tracker.record_success(node, level)
            else:
                tracker.record_failure(node, level, "Generation failed")
            
            # Progress report every 10 nodes
            if tracker.total_processed % 10 == 0:
                tracker.print_progress(tracker.total_processed, total_nodes)
        
        # Final summary
        tracker.save_checkpoint()
        
        print(f"\n[COMPLETE] GENERATION COMPLETE!")
        print(f"=" * 50)
        print(f"[PROGRESS] FINAL STATS:")
        print(f"   Total processed: {tracker.total_processed}")
        print(f"   Successful: {tracker.successful}")
        print(f"   Failed: {tracker.failed}")
        print(f"   Success rate: {(tracker.successful/max(1,tracker.total_processed)*100):.1f}%")
        print(f"   Level 2 success: {tracker.level2_stats['successful']}/{tracker.level2_stats['processed']}")
        print(f"   Level 3 success: {tracker.level3_stats['successful']}/{tracker.level3_stats['processed']}")
        
        elapsed = datetime.now() - tracker.start_time
        print(f"   Total time: {elapsed}")
        print(f"   Final cost: ${tracker.estimated_cost:.2f}")
        
        if tracker.failed_nodes:
            print(f"\n[WARNING]  FAILED NODES ({len(tracker.failed_nodes)}):")
            for failed in tracker.failed_nodes[-5:]:  # Show last 5
                print(f"   - {failed['name']} (Level {failed['level']}): {failed['error']}")
        
        if args.dry_run:
            print(f"\n[DRY_RUN] Dry run completed - no changes made")
        else:
            print(f"\n[SAVED] All descriptions saved to database!")
        
    except KeyboardInterrupt:
        print(f"\n\n[INTERRUPTED]  Interrupted by user")
        tracker.save_checkpoint()
        print(f"[CHECKPOINT] Progress saved. Resume with: --resume")
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        tracker.save_checkpoint()
        print("[CHECKPOINT] Progress saved to checkpoint")

if __name__ == "__main__":
    main()