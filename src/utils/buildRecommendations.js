function refineBuildRecommendation(preferences, componentsData) {
    const refinedRecommendations = [];

    // Iterate through components data and apply user preferences
    componentsData.forEach(component => {
        let score = 0;

        // Example preference: prioritize components with higher performance ratings
        if (preferences.performance && component.performance) {
            score += component.performance * preferences.performance.weight;
        }

        // Example preference: prioritize components with lower prices
        if (preferences.price && component.price) {
            score -= component.price * preferences.price.weight;
        }

        // Add more conditions based on user preferences

        refinedRecommendations.push({
            ...component,
            score
        });
    });

    // Sort recommendations based on the calculated score
    refinedRecommendations.sort((a, b) => b.score - a.score);

    return refinedRecommendations;
}

module.exports = {
    refineBuildRecommendation
};