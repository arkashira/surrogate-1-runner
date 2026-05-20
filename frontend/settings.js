document.addEventListener('DOMContentLoaded', () => {
    // Assuming there's an HTML element with id="settings-container" where these settings should be rendered.
    // This allows for modular injection of settings sections.
    const settingsContainer = document.getElementById('settings-container');

    if (settingsContainer) {
        // Create a new section for Cost Anomaly Alert settings
        const alertSettingsSection = document.createElement('div');
        alertSettingsSection.className = 'settings-section cost-anomaly-settings';
        alertSettingsSection.innerHTML = `
            <h2>Cost Anomaly Alert Settings</h2>
            <p>Configure the percentage increase in cost that triggers an anomaly alert.</p>
            <div class="form-group">
                <label for="anomalyThreshold">Threshold Percentage:</label>
                <input type="number" id="anomalyThreshold" value="10" min="1" max="100" step="1" aria-label="Anomaly Threshold Percentage">
                <span>%</span>
            </div>
            <button id="saveAlertSettings" class="btn btn-primary">Save Alert Settings</button>
            <div id="alertSettingsMessage" class="message" aria-live="polite"></div>
        `;
        settingsContainer.appendChild(alertSettingsSection);

        // Get references to the UI elements
        const saveButton = document.getElementById('saveAlertSettings');
        const thresholdInput = document.getElementById('anomalyThreshold');
        const messageDiv = document.getElementById('alertSettingsMessage');

        // --- Placeholder: Load existing threshold ---
        // In a real application, this would fetch the user's current threshold from a backend API.
        // For this example, we'll use localStorage to simulate persistence.
        const storedThreshold = localStorage.getItem('costAnomalyThreshold');
        if (storedThreshold !== null) {
            thresholdInput.value = storedThreshold;
        }

        // Add event listener for the save button
        saveButton.addEventListener('click', async () => {
            const newThreshold = parseFloat(thresholdInput.value);

            // Basic client-side validation
            if (isNaN(newThreshold) || newThreshold < 1 || newThreshold > 100) {
                messageDiv.textContent = 'Please enter a valid percentage between 1 and 100.';
                messageDiv.style.color = 'red';
                setTimeout(() => { messageDiv.textContent = ''; }, 3000);
                return;
            }

            // --- Placeholder: Send threshold to backend ---
            // In a real application, an API call would be made here to persist the setting.
            // Example:
            // try {
            //     const response = await fetch('/api/settings/cost-anomaly-threshold', {
            //         method: 'POST',
            //         headers: { 'Content-Type': 'application/json' },
            //         body: JSON.stringify({ threshold: newThreshold })
            //     });
            //     if (!response.ok) throw new Error('Failed to save settings');
            //     localStorage.setItem('costAnomalyThreshold', newThreshold); // Update local storage on success
            //     messageDiv.textContent = 'Settings saved successfully!';
            //     messageDiv.style.color = 'green';
            // } catch (error) {
            //     console.error('Error saving cost anomaly threshold:', error);
            //     messageDiv.textContent = 'Error saving settings. Please try again.';
            //     messageDiv.style.color = 'red';
            // }

            // Simulate successful save for demonstration
            console.log('Simulating saving new cost anomaly threshold:', newThreshold + '%');
            localStorage.setItem('costAnomalyThreshold', newThreshold.toString()); // Update local storage
            messageDiv.textContent = 'Settings saved successfully!';
            messageDiv.style.color = 'green';

            // Clear message after a few seconds
            setTimeout(() => {
                messageDiv.textContent = '';
            }, 3000);
        });
    } else {
        console.warn('Settings container not found. Ensure an element with id="settings-container" exists in your HTML to render cost anomaly alert settings.');
    }
});