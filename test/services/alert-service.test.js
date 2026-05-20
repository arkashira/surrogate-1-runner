const alertService = require('./alert-service');

describe('alertService', () => {
  it('should send email and slack notification when anomaly is detected', () => {
    const data = [1, 2, 3, 4, 5, 100];
    const threshold = 2;
    const spyEmail = jest.spyOn(require('nodemailer'), 'sendMail');
    const spySlack = jest.spyOn(require('slack'), 'chat.postMessage');
    alertService(data, threshold);
    expect(spyEmail).toHaveBeenCalledTimes(1);
    expect(spySlack).toHaveBeenCalledTimes(1);
  });
});