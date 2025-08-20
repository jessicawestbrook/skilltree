#!/usr/bin/env python3
"""
Optimized Rate Limiter for Claude API
===================================

Implements intelligent rate limiting based on Claude API limits and usage tiers.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Optional

class ClaudeRateLimiter:
    """
    Smart rate limiter for Claude API that adapts to usage tiers and token consumption.
    """
    
    def __init__(self, usage_tier: int = 1):
        self.usage_tier = usage_tier
        self.lock = threading.Lock()
        
        # Rate limits per tier (per minute)
        self.tier_limits = {
            1: {'rpm': 50, 'input_tokens': 30000, 'output_tokens': 8000},
            2: {'rpm': 100, 'input_tokens': 100000, 'output_tokens': 20000},
            3: {'rpm': 500, 'input_tokens': 500000, 'output_tokens': 100000},
            4: {'rpm': 4000, 'input_tokens': 2000000, 'output_tokens': 400000}
        }
        
        self.limits = self.tier_limits.get(usage_tier, self.tier_limits[1])
        
        # Token bucket tracking
        self.request_bucket = self.limits['rpm']
        self.input_token_bucket = self.limits['input_tokens']
        self.output_token_bucket = self.limits['output_tokens']
        
        # Last refill time
        self.last_refill = datetime.now()
        
        # Request history for adaptive delays
        self.request_history = []
        
    def _refill_buckets(self):
        """Refill token buckets based on elapsed time (token bucket algorithm)."""
        now = datetime.now()
        elapsed = (now - self.last_refill).total_seconds()
        
        if elapsed >= 1.0:  # Refill every second
            # Calculate refill amounts (per second)
            request_refill = (self.limits['rpm'] / 60) * elapsed
            input_refill = (self.limits['input_tokens'] / 60) * elapsed
            output_refill = (self.limits['output_tokens'] / 60) * elapsed
            
            # Refill buckets (don't exceed limits)
            self.request_bucket = min(self.limits['rpm'], 
                                    self.request_bucket + request_refill)
            self.input_token_bucket = min(self.limits['input_tokens'],
                                        self.input_token_bucket + input_refill)
            self.output_token_bucket = min(self.limits['output_tokens'],
                                         self.output_token_bucket + output_refill)
            
            self.last_refill = now
    
    def can_make_request(self, estimated_input_tokens: int, estimated_output_tokens: int) -> bool:
        """Check if we can make a request with estimated token usage."""
        with self.lock:
            self._refill_buckets()
            
            return (self.request_bucket >= 1 and 
                   self.input_token_bucket >= estimated_input_tokens and
                   self.output_token_bucket >= estimated_output_tokens)
    
    def wait_for_capacity(self, estimated_input_tokens: int, estimated_output_tokens: int) -> float:
        """
        Calculate how long to wait before making a request.
        Returns wait time in seconds.
        """
        with self.lock:
            self._refill_buckets()
            
            # Calculate wait times for each limit
            wait_times = []
            
            # Request limit wait time
            if self.request_bucket < 1:
                requests_needed = 1
                wait_times.append((requests_needed / (self.limits['rpm'] / 60)))
            
            # Input token limit wait time  
            if self.input_token_bucket < estimated_input_tokens:
                tokens_needed = estimated_input_tokens - self.input_token_bucket
                wait_times.append(tokens_needed / (self.limits['input_tokens'] / 60))
            
            # Output token limit wait time
            if self.output_token_bucket < estimated_output_tokens:
                tokens_needed = estimated_output_tokens - self.output_token_bucket
                wait_times.append(tokens_needed / (self.limits['output_tokens'] / 60))
            
            # Return the longest wait time needed
            return max(wait_times) if wait_times else 0
    
    def consume_tokens(self, actual_input_tokens: int, actual_output_tokens: int):
        """Record actual token consumption after API call."""
        with self.lock:
            self.request_bucket -= 1
            self.input_token_bucket -= actual_input_tokens
            self.output_token_bucket -= actual_output_tokens
            
            # Record request for adaptive optimization
            self.request_history.append({
                'timestamp': datetime.now(),
                'input_tokens': actual_input_tokens,
                'output_tokens': actual_output_tokens
            })
            
            # Keep only last 100 requests for analysis
            if len(self.request_history) > 100:
                self.request_history.pop(0)
    
    def get_optimal_delay(self) -> float:
        """
        Get optimal delay based on current tier and recent usage patterns.
        Returns delay in seconds.
        """
        # Conservative delays by tier to stay well within limits
        tier_delays = {
            1: 3.0,  # ~20 RPM (well under 50 RPM limit)  
            2: 1.5,  # ~40 RPM (well under 100 RPM limit)
            3: 0.5,  # ~120 RPM (well under 500 RPM limit) 
            4: 0.1   # ~600 RPM (well under 4000 RPM limit)
        }
        
        base_delay = tier_delays.get(self.usage_tier, 3.0)
        
        # Adaptive adjustment based on recent token usage
        if len(self.request_history) >= 5:
            recent_requests = self.request_history[-5:]
            avg_output_tokens = sum(r['output_tokens'] for r in recent_requests) / len(recent_requests)
            
            # If we're using a lot of output tokens, increase delay
            output_ratio = avg_output_tokens / (self.limits['output_tokens'] / 60)
            if output_ratio > 0.8:  # Using >80% of output token capacity
                base_delay *= 1.5
        
        return base_delay
    
    def get_status(self) -> Dict:
        """Get current rate limiter status."""
        with self.lock:
            self._refill_buckets()
            
            return {
                'usage_tier': self.usage_tier,
                'limits': self.limits,
                'current_capacity': {
                    'requests': int(self.request_bucket),
                    'input_tokens': int(self.input_token_bucket),
                    'output_tokens': int(self.output_token_bucket)
                },
                'utilization': {
                    'requests': f"{(1 - self.request_bucket/self.limits['rpm']):.1%}",
                    'input_tokens': f"{(1 - self.input_token_bucket/self.limits['input_tokens']):.1%}",
                    'output_tokens': f"{(1 - self.output_token_bucket/self.limits['output_tokens']):.1%}"
                }
            }

# Usage example and testing
def main():
    """Test the rate limiter."""
    limiter = ClaudeRateLimiter(usage_tier=1)
    
    print("=== Claude API Rate Limiter Test ===")
    print(f"Tier 1 Limits: {limiter.limits}")
    
    # Simulate content generation requests
    print("\nSimulating content generation requests...")
    
    for i in range(5):
        # Typical content generation: 1500 input + 3000 output tokens
        estimated_input = 1500
        estimated_output = 3000
        
        wait_time = limiter.wait_for_capacity(estimated_input, estimated_output)
        
        if wait_time > 0:
            print(f"Request {i+1}: Waiting {wait_time:.2f} seconds...")
            time.sleep(wait_time)
        
        print(f"Request {i+1}: Making API call...")
        
        # Simulate API call
        limiter.consume_tokens(estimated_input, estimated_output)
        
        status = limiter.get_status()
        print(f"  Output tokens remaining: {status['current_capacity']['output_tokens']}")
        
        optimal_delay = limiter.get_optimal_delay()
        print(f"  Recommended delay: {optimal_delay:.2f}s")
        time.sleep(optimal_delay)
    
    print("\n=== Final Status ===")
    final_status = limiter.get_status()
    for key, value in final_status.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()