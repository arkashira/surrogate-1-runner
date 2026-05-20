class ContentRecommendationDisplay:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.content_library = []

    def load_content_library(self):
        # Simulate loading content from a database or API
        self.content_library = [
            {"title": "Marketing Strategy 101", "description": "Learn the basics of marketing"},
            {"title": "Social Media Tips", "description": "Maximize your social media presence"},
            {"title": "Email Marketing Best Practices", "description": "Improve your email campaigns"}
        ]

    def recommend_content(self):
        recommendations = []
        for content in self.content_library:
            # Simple recommendation logic based on user profile
            if self.user_profile['goal'] == 'increase_brand_awareness':
                if 'social media' in content['description'].lower():
                    recommendations.append(content)
            elif self.user_profile['goal'] == 'boost_sales':
                if 'email marketing' in content['description'].lower():
                    recommendations.append(content)
        return recommendations

    def display_recommendations(self):
        self.load_content_library()
        recommendations = self.recommend_content()
        print("Recommended Content:")
        for rec in recommendations:
            print(f"Title: {rec['title']}, Description: {rec['description']}")

# Example usage
if __name__ == "__main__":
    user_profile = {'goal': 'increase_brand_awareness'}
    display = ContentRecommendationDisplay(user_profile)
    display.display_recommendations()