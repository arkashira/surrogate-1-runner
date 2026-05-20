import { Request, Response } from 'express';
import { hash } from 'bcrypt';
import { pool } from '../db';
import { sendEmail } from '../services/email';

interface PasswordResetRequest {
  token: string;
  newPassword: string;
}

interface ResetTokenPayload {
  userId: string;
  exp: number;
  purpose: 'password_reset';
}

/**
 * Validates password reset token and checks database
 */
async function validateResetToken(token: string): Promise<ResetTokenPayload | null> {
  try {
    const decoded = Buffer.from(token, 'base64').toString('utf-8');
    const payload: ResetTokenPayload = JSON.parse(decoded);

    if (payload.exp < Date.now()) return null;

    const result = await pool.query(
      'SELECT id FROM password_reset_tokens WHERE token = $1 AND used = FALSE AND expires_at > NOW()',
      [token]
    );

    return result.rows.length ? payload : null;
  } catch (error) {
    return null;
  }
}

/**
 * Main password reset confirmation handler
 */
export async function confirmPasswordReset(req: Request, res: Response): Promise<void> {
  try {
    const { token, newPassword } = req.body as PasswordResetRequest;

    // Input validation
    if (!token || !newPassword) {
      return res.status(400).json({
        success: false,
        error: 'Token and new password are required'
      });
    }

    // Password strength validation
    if (newPassword.length < 12) {
      return res.status(400).json({
        success: false,
        error: 'Password must be at least 12 characters'
      });
    }

    // Token validation
    const payload = await validateResetToken(token);
    if (!payload) {
      return res.status(400).json({
        success: false,
        error: 'Invalid or expired reset token'
      });
    }

    // Password hashing
    const passwordHash = await hash(newPassword, 12);

    // Database transaction
    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      // Update user password
      await client.query(
        'UPDATE users SET password_hash = $1, updated_at = NOW() WHERE id = $2',
        [passwordHash, payload.userId]
      );

      // Invalidate all tokens for this user
      await client.query(
        'UPDATE password_reset_tokens SET used = TRUE WHERE user_id = $1',
        [payload.userId]
      );

      await client.query('COMMIT');

      // Send confirmation email
      const userResult = await client.query(
        'SELECT email FROM users WHERE id = $1',
        [payload.userId]
      );

      if (userResult.rows.length) {
        await sendEmail({
          to: userResult.rows[0].email,
          subject: 'Password Reset Successful',
          template: 'password-reset-confirmation',
          data: { timestamp: new Date().toISOString() }
        });
      }

      res.status(200).json({
        success: true,
        message: 'Password has been reset successfully'
      });

    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('Password reset error:', error);
    res.status(500).json({
      success: false,
      error: 'An error occurred during password reset'
    });
  }
}