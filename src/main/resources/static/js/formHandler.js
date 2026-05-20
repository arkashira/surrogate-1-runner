document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const payload = Object.fromEntries(formData.entries());
    
    fetch('/api/marketing-strategy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = '/strategy-results?strategyId=' + data.id;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to generate strategy. Please try again.');
    });
});