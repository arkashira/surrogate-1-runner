package com.axentx.complianceguardian.ui;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class NotificationPreferencesController {

    private final NotificationPreferencesService notificationPreferencesService;

    public NotificationPreferencesController(NotificationPreferencesService notificationPreferencesService) {
        this.notificationPreferencesService = notificationPreferencesService;
    }

    @GetMapping("/notification-preferences")
    public String getNotificationPreferences(Model model) {
        model.addAttribute("notificationPreferences", notificationPreferencesService.getNotificationPreferences());
        return "notification-preferences";
    }

    @PostMapping("/notification-preferences")
    public String updateNotificationPreferences(@RequestParam boolean emailNotifications,
                                               @RequestParam boolean slackNotifications,
                                               @RequestParam boolean disabled) {
        notificationPreferencesService.updateNotificationPreferences(emailNotifications, slackNotifications, disabled);
        return "redirect:/notification-preferences";
    }
}

// opt/axentx/surrogate-1/ui/src/main/resources/templates/notification-preferences.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Notification Preferences</title>
</head>
<body>
<h1>Notification Preferences</h1>
<form action="#" th:action="@{/notification-preferences}" th:object="${notificationPreferences}" method="post">
    <input type="checkbox" th:field="*{emailNotifications}"> Email Notifications<br>
    <input type="checkbox" th:field="*{slackNotifications}"> Slack Notifications<br>
    <input type="checkbox" th:field="*{disabled}"> Disable Notifications<br>
    <input type="submit" value="Save">
</form>
</body>
</html>

// opt/axentx/surrogate-1/service/src/main/java/com/axentx/complianceguardian/service/NotificationPreferencesService.java
package com.axentx.complianceguardian.service;

import org.springframework.stereotype.Service;

@Service
public class NotificationPreferencesService {

    private boolean emailNotifications = true;
    private boolean slackNotifications = true;
    private boolean disabled = false;

    public NotificationPreferences getNotificationPreferences() {
        return new NotificationPreferences(emailNotifications, slackNotifications, disabled);
    }

    public void updateNotificationPreferences(boolean emailNotifications, boolean slackNotifications, boolean disabled) {
        this.emailNotifications = emailNotifications;
        this.slackNotifications = slackNotifications;
        this.disabled = disabled;
    }
}

// opt/axentx/surrogate-1/service/src/main/java/com/axentx/complianceguardian/service/NotificationPreferences.java
package com.axentx.complianceguardian.service;

public class NotificationPreferences {
    private boolean emailNotifications;
    private boolean slackNotifications;
    private boolean disabled;

    public NotificationPreferences(boolean emailNotifications, boolean slackNotifications, boolean disabled) {
        this.emailNotifications = emailNotifications;
        this.slackNotifications = slackNotifications;
        this.disabled = disabled;
    }

    // getters and setters
}

## Summary
- Added `NotificationPreferences` class to hold notification preferences
- Created `NotificationPreferencesService` to manage notification preferences
- Added `NotificationPreferencesController` to handle UI requests for notification preferences
- Created `notification-preferences.html` template for the notification preferences UI
- Updated `NotificationPreferencesService` to update notification preferences based on user input