import { Test, TestingModule } from '@nestjs/testing';
import { AuthGuard } from '../guards/authGuard';
import { AuthService } from '../services/authService';

describe('AuthGuard', () => {
  let authGuard: AuthGuard;
  let authService: AuthService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AuthGuard, AuthService],
    }).compile();

    authGuard = module.get<AuthGuard>(AuthGuard);
    authService = module.get<AuthService>(AuthService);
  });

  it('should validate user credentials and roles', async () => {
    jest.spyOn(authService, 'validateUser').mockResolvedValue(true);
    jest.spyOn(authService, 'getUserRoles').mockResolvedValue(['shell_access']);
    jest.spyOn(authService, 'logAuthenticationEvent').mockImplementation();

    const request = {
      body: {
        username: 'testUser',
        password: 'testPassword',
      },
    };

    const result = await authGuard.canActivate({ switchToHttp: () => ({ getRequest: () => request }) } as any);

    expect(result).toBe(true);
    expect(authService.validateUser).toHaveBeenCalledWith('testUser', 'testPassword');
    expect(authService.getUserRoles).toHaveBeenCalledWith('testUser');
    expect(authService.logAuthenticationEvent).toHaveBeenCalledWith('testUser', 'shell_session_initiated');
  });
});