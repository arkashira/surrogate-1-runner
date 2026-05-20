document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = form.elements['username'].value.trim();
        const password = form.elements['password'].value.trim();

        if (!username || !password) {
            alert('Username and password are required.');
            return;
        }

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const text = await response.text();
            if (response.ok) {
                alert(text);
                form.reset();
            } else {
                alert(`Error (${response.status}): ${text}`);
            }
        } catch (err) {
            console.error(err);
            alert('Network error while registering.');
        }
    });
});