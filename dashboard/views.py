from django.shortcuts import render
from django.views import View
from django.db.models import Sum, Avg
from .models import UsageLog, PerformanceMetric

def get_cost_recommendations():
    """Generate cost optimization recommendations based on usage and performance data."""
    recommendations = []
    
    # Check for high token usage patterns
    high_token_usage = UsageLog.objects.filter(token_count__gt=1000).count() > 50
    if high_token_usage:
        recommendations.append({
            'title': 'Reduce High Token Costs',
            'description': 'Detected frequent high-token requests (>1000 tokens). Consider:',
            'actions': [
                'Implement input truncation for long prompts',
                'Use cost-effective models for batch processing',
                'Add token usage limits to API rate limits'
            ]
        })
    
    # Check for low accuracy models
    low_accuracy_models = PerformanceMetric.objects.filter(accuracy__lt=0.7).exists()
    if low_accuracy_models:
        recommendations.append({
            'title': 'Optimize Model Selection',
            'description': 'Some models show low accuracy (<70%). Consider:',
            'actions': [
                'Replace with fine-tuned variants for specific tasks',
                'Implement model routing based on input patterns',
                'Add accuracy monitoring thresholds'
            ]
        })
    
    # Check for inefficient resource usage
    slow_responses = PerformanceMetric.objects.filter(response_time__gt=2.0).count() > 10
    if slow_responses:
        recommendations.append({
            'title': 'Improve Response Efficiency',
            'description': 'Detected slow response times (>2s). Consider:',
            'actions': [
                'Enable caching for repeated queries',
                'Optimize database queries',
                'Scale compute resources during peak hours'
            ]
        })
    
    return recommendations

class DashboardView(View):
    def get(self, request):
        # Get usage statistics
        usage_stats = UsageLog.objects.aggregate(
            total_tokens=Sum('token_count'),
            avg_latency=Avg('response_time')
        )
        
        # Generate recommendations
        recommendations = get_cost_recommendations()
        
        context = {
            'usage_stats': usage_stats,
            'recommendations': recommendations
        }
        return render(request, 'dashboard.html', context)