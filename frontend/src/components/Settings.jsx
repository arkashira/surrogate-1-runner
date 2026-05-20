import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Settings() {
    const [emailNotifications, setEmailNotifications] = useState(true);

    useEffect(() => {
        axios.get('/api/user/preferences')
            .then(response => {
                setEmailNotifications(response.data.email_notifications);
            })
            .catch(error => {
                console.error(error);
            });
    }, []);

    const handleToggle = () => {
        axios.patch('/api/user/preferences', { email_notifications: !emailNotifications })
            .then(response => {
                setEmailNotifications(response.data.email_notifications);
            })
            .catch(error => {
                console.error(error);
            });
    };

    return (
        <div>
            <label>
                Email Notifications:
                <input type="checkbox" checked={emailNotifications} onChange={handleToggle} />
            </label>
        </div>
    );
}

export default Settings;