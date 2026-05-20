import React from 'react';
import Tooltip from './Tooltip';

const Form = () => {
  return (
    <form>
      <label>
        <Tooltip text="This is a required field">
          <input type="text" required />
        </Tooltip>
      </label>
    </form>
  );
};

export default Form;