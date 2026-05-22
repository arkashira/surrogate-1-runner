import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  isFreeTier: boolean;
}

const initialState: UserState = {
  isFreeTier: false,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setFreeTier: (state, action: PayloadAction<boolean>) => {
      state.isFreeTier = action.payload;
    },
  },
});

export const { setFreeTier } = userSlice.actions;
export default userSlice.reducer;