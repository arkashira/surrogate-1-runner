document.addEventListener('DOMContentLoaded', () => {
    const alertsContainer = document.getElementById('alerts-container');
    const costDetails = document.getElementById('cost-details');

    function displayAlert(alert) {
        const alertElement = document.createElement('div');
        alertElement.className = 'alert';
        alertElement.textContent = `Alert: ${alert.message} - Estimated Savings: $${alert.savings.toFixed(2)}`;
        alertsContainer.appendChild(alertElement);
    }

    function fetchAlerts() {
        fetch('/api/alerts')
            .then(response => response.json())
            .then(data => {
                data.forEach(alert => displayAlert(alert));
            })
            .catch(error => console.error('Error fetching alerts:', error));
    }

    function customizeAlerts() {
        // Placeholder for customization logic
        console.log('Customizing alerts...');
    }

    fetchAlerts();
    customizeAlerts();
});