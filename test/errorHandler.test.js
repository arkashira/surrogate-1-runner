const errorHandler = require('../src/errorHandler');
const logger = require('../src/logger');

jest.mock('../src/logger', () => ({
    error: jest.fn(),
}));

describe('handleVerificationError', () => {
    it('should log an error and throw an exception', () => {
        const error = new Error('Test error');
        const moduleName = 'testModule';

        expect(() => errorHandler.handleVerificationError(error, moduleName)).toThrow();
        expect(logger.error).toHaveBeenCalledWith(expect.stringContaining('Verification error in testModule'));
    });
});