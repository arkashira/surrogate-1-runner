import { Dispatch } from 'redux';
import { UpgradeActionTypes, FETCH_UPGRADE_RECOMMENDATIONS } from '../types/upgradeTypes';
import { fetchRecommendations } from '../../services/upgradeService';

export const fetchUpgradeRecommendations = (budget: number, targetGame: string) => {
  return async (dispatch: Dispatch<UpgradeActionTypes>) => {
    dispatch({ type: FETCH_UPGRADE_RECOMMENDATIONS });
    try {
      const recommendations = await fetchRecommendations(budget, targetGame);
      dispatch({
        type: FETCH_UPGRADE_RECOMMENDATIONS_SUCCESS,
        payload: recommendations,
      });
    } catch (error) {
      dispatch({
        type: FETCH_UPGRADE_RECOMMENDATIONS_FAILURE,
        payload: error.message,
      });
    }
  };
};