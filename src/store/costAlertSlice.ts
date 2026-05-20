import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface CostAlertState {
  isVisible: boolean;
  commitSha: string;
  cost: number;
}

const initialState: CostAlertState = {
  isVisible: false,
  commitSha: '',
  cost: 0,
};

export const costAlertSlice = createSlice({
  name: 'costAlert',
  initialState,
  reducers: {
    /** Show the banner for a specific commit */
    showCostAlert: (
      state,
      action: PayloadAction<{ commitSha: string; cost: number }>,
    ) => {
      state.isVisible = true;
      state.commitSha = action.payload.commitSha;
      state.cost = action.payload.cost;
    },

    /** Hide the banner (used by the dismiss button or auto‑hide) */
    hideCostAlert: (state) => {
      state.isVisible = false;
    },
  },
});

export const { showCostAlert, hideCostAlert } = costAlertSlice.actions;
export default costAlertSlice.reducer;