#!/usr/bin/env python3
"""
Analyze our current content generation against Claude API rate limits.
"""

def analyze_content_generation_rates():
    """Analyze token usage for our content generation system."""
    
    print("=== Claude API Rate Limit Analysis ===")
    print("For SkillTree Content Generation System\n")
    
    # Current system parameters
    current_delay = 2.0  # seconds between requests
    requests_per_minute = 60 / current_delay
    
    # Estimated token usage per request (based on our generated content)
    avg_input_tokens = 1500   # Prompt + content preview
    avg_output_tokens = 3000  # Generated content + questions
    
    print("📊 Current System Performance:")
    print(f"  Delay between requests: {current_delay}s")
    print(f"  Effective rate: {requests_per_minute:.1f} requests/minute")
    print(f"  Input tokens/minute: {requests_per_minute * avg_input_tokens:,.0f}")
    print(f"  Output tokens/minute: {requests_per_minute * avg_output_tokens:,.0f}")
    
    # Claude API Tier 1 limits
    tier1_limits = {
        'rpm': 50,
        'input_tokens': 30000,
        'output_tokens': 8000
    }
    
    print(f"\n🔒 Claude API Tier 1 Limits:")
    print(f"  Requests: {tier1_limits['rpm']} per minute")
    print(f"  Input tokens: {tier1_limits['input_tokens']:,} per minute")
    print(f"  Output tokens: {tier1_limits['output_tokens']:,} per minute")
    
    # Usage analysis
    print(f"\n📈 Usage Analysis:")
    request_utilization = (requests_per_minute / tier1_limits['rpm']) * 100
    input_utilization = (requests_per_minute * avg_input_tokens / tier1_limits['input_tokens']) * 100
    output_utilization = (requests_per_minute * avg_output_tokens / tier1_limits['output_tokens']) * 100
    
    print(f"  Request utilization: {request_utilization:.1f}% ({'✅ OK' if request_utilization <= 80 else '⚠️ HIGH'})")
    print(f"  Input token utilization: {input_utilization:.1f}% ({'✅ OK' if input_utilization <= 80 else '⚠️ HIGH'})")
    print(f"  Output token utilization: {output_utilization:.1f}% ({'✅ OK' if output_utilization <= 80 else '❌ OVER LIMIT'})")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    if output_utilization > 100:
        safe_delay = (requests_per_minute * avg_output_tokens) / (tier1_limits['output_tokens'] * 0.8) * current_delay
        print(f"  🚨 OUTPUT TOKEN LIMIT EXCEEDED!")
        print(f"  Recommended delay: {safe_delay:.1f}s (vs current {current_delay}s)")
        print(f"  This reduces rate to {60/safe_delay:.1f} requests/minute")
    elif max(request_utilization, input_utilization, output_utilization) > 80:
        print(f"  ⚠️ Operating near limits - current delays are appropriate")
    else:
        faster_delay = current_delay * 0.7  # Could go 30% faster
        print(f"  ✅ Could run faster - try {faster_delay:.1f}s delay")
    
    # Cost projection
    print(f"\n💰 Cost Analysis:")
    
    # Claude 3 Haiku pricing (as of 2025): ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
    input_cost_per_1m = 0.25
    output_cost_per_1m = 1.25
    
    cost_per_request = (avg_input_tokens * input_cost_per_1m / 1000000) + (avg_output_tokens * output_cost_per_1m / 1000000)
    cost_per_hour = cost_per_request * requests_per_minute * 60
    
    print(f"  Cost per request: ${cost_per_request:.4f}")
    print(f"  Cost per hour: ${cost_per_hour:.2f}")
    print(f"  740 topics cost: ${740 * cost_per_request:.2f}")
    
    # Tier upgrade analysis
    print(f"\n🎯 Tier Upgrade Benefits:")
    tier4_rpm = 4000 / 60  # Can do much faster
    optimal_delay_tier4 = 1.0  # 1 second delay for safety
    tier4_rate = 60 / optimal_delay_tier4
    
    print(f"  Tier 4 safe rate: {tier4_rate:.0f} requests/minute")
    print(f"  Time for 740 topics:")
    print(f"    Current (Tier 1): {740 / requests_per_minute:.1f} minutes")
    print(f"    With Tier 4: {740 / tier4_rate:.1f} minutes")
    
if __name__ == "__main__":
    analyze_content_generation_rates()