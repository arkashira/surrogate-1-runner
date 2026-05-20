document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('metric-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const metricName = document.getElementById('metric-name').value;
        const metricType = document.getElementById('metric-type').value;
        const valueDistribution = document.getElementById('value-distribution').value;
        const emissionInterval = document.getElementById('emission-interval').value;

        // Simulate saving the form data (replace with actual API call)
        console.log(`Saved preset: ${metricName}, ${metricType}, ${valueDistribution}, ${emissionInterval}`);

        // Clear the form after submission
        form.reset();
    });
});