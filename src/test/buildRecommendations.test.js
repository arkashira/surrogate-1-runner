const { refineBuildRecommendation } = require('../utils/buildRecommendations');
const componentsData = require('../data/components.json');

describe('refineBuildRecommendation', () => {
    it('should refine build recommendations based on user preferences', () => {
        const preferences = {
            performance: { weight: 0.6 },
            price: { weight: 0.4 }
        };

        const refinedRecommendations = refineBuildRecommendation(preferences, componentsData);

        expect(refinedRecommendations.length).toBe(componentsData.length);
        expect(refinedRecommendations[0].score).toBeGreaterThan(refinedRecommendations[1].score);
        expect(refinedRecommendations[1].score).toBeGreaterThan(refinedRecommendations[2].score);
    });
});