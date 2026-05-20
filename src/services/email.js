export const sendWelcomeEmail = async (data) => {
  console.log('Sending welcome email:', data);
  
  // Simulate API call
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, messageId: 'msg_' + Date.now() });
    }, 500);
  });
};

export const sendTemplateConfirmation = async (templateId, workflowName) => {
  console.log('Sending template confirmation:', { templateId, workflowName });
  return { success: true };
};