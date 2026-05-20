import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { api } from '../../api/api';

export type SandboxStatus =
  | 'idle'
  | 'creating'
  | 'provisioning'
  | 'ready'
  | 'error';

export interface SandboxState {
  status: SandboxStatus;
  error: string | null;
}

const initialState: SandboxState = {
  status: 'idle',
  error: null,
};

/**
 * Fetch the current sandbox status from the API.
 * The thunk automatically generates
 *   - sandbox/fetchStatus/pending
 *   - sandbox/fetchStatus/fulfilled
 *   - sandbox/fetchStatus/rejected
 */
export const fetchSandboxStatus = createAsyncThunk<
  SandboxStatus,
  void,
  { rejectValue: string }
>('sandbox/fetchStatus', async (_, { rejectWithValue }) => {
  try {
    const { data } = await api.get<{ status: SandboxStatus }>('/sandbox/status');
    return data.status;
  } catch (err: any) {
    return rejectWithValue(err.message ?? 'Unknown error');
  }
});

const sandboxSlice = createSlice({
  name: 'sandbox',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchSandboxStatus.pending, (state) => {
        state.status = 'creating';
        state.error = null;
      })
      .addCase(fetchSandboxStatus.fulfilled, (state, action: PayloadAction<SandboxStatus>) => {
        state.status = action.payload;
        state.error = null;
      })
      .addCase(fetchSandboxStatus.rejected, (state, action) => {
        state.status = 'error';
        state.error = action.payload as string;
      });
  },
});

export default sandboxSlice.reducer;