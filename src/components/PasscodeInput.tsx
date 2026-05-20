import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { encryptData, decryptData, wipeData } from '../utils/encryption';
import { setPasscode, incrementRetryCount, resetRetryCount } from '../store/actions';

const PasscodeInput = () => {
  const [passcode, setPasscode] = useState('');
  const [error, setError] = useState('');
  const dispatch = useDispatch();
  const retryCount = useSelector((state) => state.retryCount);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const encryptedData = await encryptData(passcode);
      dispatch(setPasscode(passcode));
      dispatch(resetRetryCount());
    } catch (err) {
      setError('Incorrect passcode');
      dispatch(incrementRetryCount());
      if (retryCount >= 4) {
        const confirmWipe = window.confirm('You have entered the incorrect passcode 5 times. Your data will be wiped. Are you sure?');
        if (confirmWipe) {
          wipeData();
        }
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={passcode}
          onChange={(e) => setPasscode(e.target.value)}
          placeholder="Enter your passcode"
        />
        <button type="submit">Submit</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};

export default PasscodeInput;