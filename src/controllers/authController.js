const bcrypt = require('bcrypt');
const User = require('../models/User');

/**
 * Handles advisor sign-up.
 *
 * Expected payload:
 *   {
 *     "email": "advisor@example.com",
 *     "password": "plain-text-password"
 *   }
 *
 * On success returns 201 with the created user (sans password hash).
 */
async function signup(req, res) {
  try {
    const { email, password } = req.body;

    // Basic validation
    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required.' });
    }

    // Check for existing user
    const existing = await User.findOne({ email: email.toLowerCase() });
    if (existing) {
      return res.status(409).json({ error: 'User with this email already exists.' });
    }

    // Hash password
    const saltRounds = 10;
    const passwordHash = await bcrypt.hash(password, saltRounds);

    // Create advisor user
    const user = new User({
      email: email.toLowerCase(),
      passwordHash,
      role: 'advisor',
    });

    await user.save();

    // Return created user (omit passwordHash)
    const { passwordHash: _, ...userData } = user.toObject();
    return res.status(201).json({ user: userData });
  } catch (err) {
    console.error('Signup error:', err);
    return res.status(500).json({ error: 'Internal server error.' });
  }
}

module.exports = {
  signup,
};