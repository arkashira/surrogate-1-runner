export async function notifyUser(resources: any[]) {
  // Simulate user notification
  console.log('Notifying users...');
  // Here you can add the actual logic to send notifications to users
  resources.forEach(resource => {
    console.log(`Notification sent for resource: ${resource.id}`);
  });
  return Promise.resolve();
}