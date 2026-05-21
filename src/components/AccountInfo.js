import React from 'react';
import PropTypes from 'prop-types';

const AccountInfo = ({ account }) => {
  if (!account) {
    return <div>No account connected</div>;
  }

  return (
    <div className="account-info">
      <h2>Connected Account</h2>
      <p><strong>Brokerage:</strong> {account.brokerageName}</p>
      <p><strong>Account Number:</strong> {account.accountNumber}</p>
      <p><strong>Balance:</strong> ${account.balance.toFixed(2)}</p>
      <p><strong>Account Type:</strong> {account.accountType}</p>
      <button onClick={() => account.onDisconnect()}>Disconnect Account</button>
    </div>
  );
};

AccountInfo.propTypes = {
  account: PropTypes.shape({
    brokerageName: PropTypes.string,
    accountNumber: PropTypes.string,
    balance: PropTypes.number,
    accountType: PropTypes.string,
    onDisconnect: PropTypes.func,
  }),
};

export default AccountInfo;