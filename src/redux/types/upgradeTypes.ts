export const FETCH_UPGRADE_RECOMMENDATIONS = 'FETCH_UPGRADE_RECOMMENDATIONS';
export const FETCH_UPGRADE_RECOMMENDATIONS_SUCCESS = 'FETCH_UPGRADE_RECOMMENDATIONS_SUCCESS';
export const FETCH_UPGRADE_RECOMMENDATIONS_FAILURE = 'FETCH_UPGRADE_RECOMMENDATIONS_FAILURE';

interface FetchUpgradeRecommendationsAction {
  type: typeof FETCH_UPGRADE_RECOMMENDATIONS;
}

interface FetchUpgradeRecommendationsSuccessAction {
  type: typeof FETCH_UPGRADE_RECOMMENDATIONS_SUCCESS;
  payload: any[];
}

interface FetchUpgradeRecommendationsFailureAction {
  type: typeof FETCH_UPGRADE_RECOMMENDATIONS_FAILURE;
  payload: string;
}

export type UpgradeActionTypes =
  | FetchUpgradeRecommendationsAction
  | FetchUpgradeRecommendationsSuccessAction
  | FetchUpgradeRecommendationsFailureAction;