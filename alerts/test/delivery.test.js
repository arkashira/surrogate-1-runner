const delivery = require('../delivery');
const { sendEmailAlert } = require('../email');
const { sendSMSAlert } = require('../sms');

jest.mock('../email', () => ({
  sendEmailAlert: jest.fn()
}));

jest.mock('../sms', () => ({
  sendSMSAlert: jest.fn()
}));

describe('Alert Delivery', () => {
  it('should deliver alerts via email and SMS', async () => {
    const alertData = {
      recipientEmail: 'test@example.com',
      recipientPhone: '+1234567890',
      message: 'Test alert message'
    };

    await delivery.deliverAlert(alertData);

    expect(sendEmailAlert).toHaveBeenCalledWith(alertData);
    expect(sendSMSAlert).toHaveBeenCalledWith(alertData);
  });
});