import { START_CALIBRATION, ADJUST_GAIN, CALIBRATION_COMPLETE } from './audio_actions';

const initialState = {
  isCalibrating: false,
  inputLevel: -6,
  calibrationHistory: [],
  lastCalibration: null,
};

const audioReducer = (state = initialState, action) => {
  switch (action.type) {
    case START_CALIBRATION:
      return {
        ...state,
        isCalibrating: true,
        calibrationHistory: [...state.calibrationHistory, {
          timestamp: Date.now(),
          level: state.inputLevel,
          status: 'started'
        }]
      };
    
    case ADJUST_GAIN:
      return {
        ...state,
        inputLevel: action.payload,
        calibrationHistory: [...state.calibrationHistory, {
          timestamp: Date.now(),
          level: action.payload,
          status: 'adjusted'
        }]
      };
    
    case CALIBRATION_COMPLETE:
      return {
        ...state,
        isCalibrating: false,
        lastCalibration: {
          timestamp: Date.now(),
          level: state.inputLevel
        },
        calibrationHistory: [...state.calibrationHistory, {
          timestamp: Date.now(),
          level: state.inputLevel,
          status: 'completed'
        }]
      };
    
    default:
      return state;
  }
};

export default audioReducer;