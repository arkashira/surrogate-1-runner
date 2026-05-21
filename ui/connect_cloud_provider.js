document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cloudProviderForm');
    const statusMessage = document.getElementById('statusMessage');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const providerData = {
            providerType: formData.get('providerType'),
            accessKey: formData.get('accessKey'),
            secretKey: formData.get('secretKey'),
            region: formData.get('region')
        };

        // Show loading state
        statusMessage.innerHTML = '<p>Connecting...</p>';
        statusMessage.className = 'loading';

        try {
            // Send request to backend
            const response = await fetch('/api/cloud-providers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(providerData)
            });

            const result = await response.json();

            if (response.ok) {
                statusMessage.innerHTML = `<p style="color: green;">Successfully connected to ${providerData.providerType}!</p>`;
                statusMessage.className = 'success';
                
                // Reset form
                form.reset();
            } else {
                throw new Error(result.message || 'Failed to connect provider');
            }
        } catch (error) {
            statusMessage.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            statusMessage.className = 'error';
        }
    });
});