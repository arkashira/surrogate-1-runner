import { UpgradeActionTypes, FETCH_UPGRADE_RECOMMENDATIONS, FETCH_UPGRADE_RECOMMENDATIONS_SUCCESS, FETCH_UPGRADE_RECOMMENDATIONS_FAILURE } from '../types/upgradeTypes';

interface UpgradeState {
  recommendations: any[];
  loading: boolean;
  error: string | null;
}

const initialState: UpgradeState = {
  recommendations: [],
  loading: false,
  error: null,
};

const upgradeReducer = (state = initialState, action: UpgradeActionTypes): UpgradeState => {
  switch (action.type) {
    case FETCH_UPGRADE_RECOMMENDATIONS:
      return {
        ...state,
        loading: true,
        error: null,
      };
    case FETCH_UPGRADE_RECOMMENDATIONS_SUCCESS:
      return {
        ...state,
        loading: false,
        recommendations: action.payload,
      };
    case FETCH_UPGRADE_RECOMMENDATIONS_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    default:
      return state;
  }
};

export default upgradeReducer;