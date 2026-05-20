function getCostOptimizationRecommendations() {
    // Mock data for demonstration purposes
    const recommendations = [
        {
            title: 'Reduce Cloud Storage Costs',
            description: 'Optimize cloud storage usage by deleting unused files and compressing large files.',
            action: 'Review and manage your cloud storage settings.'
        },
        {
            title: 'Negotiate Better Deals with Vendors',
            description: 'Reach out to your current vendors to negotiate better pricing or discounts based on volume purchases.',
            action: 'Contact your vendor representatives to discuss potential savings.'
        },
        {
            title: 'Implement Energy-Efficient Practices',
            description: 'Reduce energy consumption by upgrading to energy-efficient equipment and implementing smart power management practices.',
            action: 'Research and invest in energy-efficient solutions for your business.'
        }
    ];

    return recommendations.slice(0, 3);
}

function displayRecommendations() {
    const recommendations = getCostOptimizationRecommendations();
    const recommendationsContainer = document.getElementById('recommendations-container');

    recommendations.forEach(recommendation => {
        const recommendationElement = document.createElement('div');
        recommendationElement.className = 'recommendation';

        const titleElement = document.createElement('h3');
        titleElement.textContent = recommendation.title;
        recommendationElement.appendChild(titleElement);

        const descriptionElement = document.createElement('p');
        descriptionElement.textContent = recommendation.description;
        recommendationElement.appendChild(descriptionElement);

        const actionElement = document.createElement('p');
        actionElement.textContent = recommendation.action;
        recommendationElement.appendChild(actionElement);

        recommendationsContainer.appendChild(recommendationElement);
    });
}

// Call the function to display recommendations when the page loads
window.onload = displayRecommendations;