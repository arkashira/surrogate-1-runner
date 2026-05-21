from expert_insights import ExpertInsights

def main():
    api_key = "your_api_key_here"
    expert_insights = ExpertInsights(api_key)
    component_id = "example_component_id"

    insights = expert_insights.get_insights(component_id)
    print("Expert Insights:", insights)

    recommendations = expert_insights.get_recommendations(component_id)
    print("Expert Recommendations:", recommendations)

if __name__ == "__main__":
    main()