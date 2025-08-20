#!/usr/bin/env python3

# Simple rate limit analysis
current_delay = 2.0
requests_per_minute = 60 / current_delay
avg_input_tokens = 1500
avg_output_tokens = 3000

print('=== Claude API Rate Limit Analysis ===')
print('Current System:')
print(f'  Requests per minute: {requests_per_minute:.1f}')
print(f'  Input tokens/min: {requests_per_minute * avg_input_tokens:,.0f}')
print(f'  Output tokens/min: {requests_per_minute * avg_output_tokens:,.0f}')

print()
print('Claude API Tier 1 Limits:')
print('  Requests: 50 per minute')
print('  Input tokens: 30,000 per minute') 
print('  Output tokens: 8,000 per minute')

print()
print('Usage Analysis:')
request_util = (requests_per_minute / 50) * 100
input_util = (requests_per_minute * avg_input_tokens / 30000) * 100
output_util = (requests_per_minute * avg_output_tokens / 8000) * 100

print(f'  Request utilization: {request_util:.1f}%')
print(f'  Input token utilization: {input_util:.1f}%')
print(f'  Output token utilization: {output_util:.1f}%')

print()
if output_util > 100:
    safe_delay = (requests_per_minute * avg_output_tokens) / (8000 * 0.8) * current_delay
    print('ISSUE: OUTPUT TOKEN LIMIT EXCEEDED!')
    print(f'Recommended delay: {safe_delay:.1f}s (current: {current_delay}s)')
    print('This will keep us within the 8,000 output tokens/minute limit')
else:
    print('Rate limiting looks good!')

print()
print('Cost estimate:')
cost_per_request = (avg_input_tokens * 0.25 / 1000000) + (avg_output_tokens * 1.25 / 1000000)
print(f'Cost per request: ${cost_per_request:.4f}')
print(f'740 topics total cost: ${740 * cost_per_request:.2f}')