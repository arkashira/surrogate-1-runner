const { DataTypes, Op } = require('sequelize');
const sequelize = require('../db');
const logger = require('../utils/logger');

const RetirementAccount = sequelize.define(
  'RetirementAccount',
  {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true,
    },
    userId: {
      type: DataTypes.UUID,
      allowNull: false,
    },
    provider: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    accountId: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    accessToken: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    refreshToken: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    tokenExpiresAt: {
      type: DataTypes.DATE,
      allowNull: true,
    },
    lastSyncedAt: {
      type: DataTypes.DATE,
      allowNull: true,
    },
    data: {
      type: DataTypes.JSONB,
      allowNull: true,
    },
  },
  {
    tableName: 'retirement_accounts',
    timestamps: true,
    indexes: [
      {
        unique: true,
        fields: ['userId', 'provider', 'accountId'],
      },
    ],
  }
);

/**
 * Refresh the OAuth token if it has expired.
 * Returns `true` if the token was refreshed, otherwise `false`.
 */
RetirementAccount.prototype.refreshTokenIfNeeded = async function () {
  if (!this.refreshToken) return false;

  const now = new Date();
  if (this.tokenExpiresAt && this.tokenExpiresAt > now) return false;

  try {
    const { accessToken, expiresIn } = await require('../api/providerAuth').refreshToken(
      this.refreshToken
    );
    this.accessToken = accessToken;
    this.tokenExpiresAt = new Date(now.getTime() + expiresIn * 1000);
    await this.save({ fields: ['accessToken', 'tokenExpiresAt'] });
    logger.info(`Refreshed token for account ${this.accountId}`);
    return true;
  } catch (err) {
    logger.error(`Failed to refresh token for account ${this.accountId}: ${err.message}`);
    throw err;
  }
};

module.exports = RetirementAccount;