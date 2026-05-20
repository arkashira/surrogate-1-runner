import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Observable } from 'rxjs';
import { AuthService } from '../services/authService';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private readonly authService: AuthService) {}

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    return this.validateRequest(request);
  }

  private async validateRequest(request: any): Promise<boolean> {
    const { username, password } = request.body;
    const isValidUser = await this.authService.validateUser(username, password);

    if (!isValidUser) {
      return false;
    }

    // Check RBAC here based on user roles
    const userRoles = await this.authService.getUserRoles(username);
    const requiredRole = 'shell_access'; // Define required role for shell access

    if (!userRoles.includes(requiredRole)) {
      return false;
    }

    // Log authentication event for audit purposes
    this.authService.logAuthenticationEvent(username, 'shell_session_initiated');

    return true;
  }
}