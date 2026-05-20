export const START_CALIBRATION = 'START_CALIBRATION';
export const ADJUST_GAIN = 'ADJUST_GAIN';
export const CALIBRATION_COMPLETE = 'CALIBRATION_COMPLETE';

export const startCalibration = () => ({
  type: START_CALIBRATION,
});

export const adjustGain = (newLevel) => ({
  type: ADJUST_GAIN,
  payload: newLevel,
});

export const completeCalibration = () => ({
  type: CALIBRATION_COMPLETE,
});