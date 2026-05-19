import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { FormattingRules } from '../types/rules';

const STORAGE_KEY = 'formattingRules';

const loadFromStorage = (): FormattingRules => {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) return defaultRules;
  try {
    return JSON.parse(stored) as FormattingRules;
  } catch {
    return defaultRules;
  }
};

const defaultRules: FormattingRules = {
  indentSize: 2,
  tabSize: 2,
  endOfLine: 'lf',
  insertSpaces: true,
};

const rulesSlice = createSlice({
  name: 'rules',
  initialState: loadFromStorage(),
  reducers: {
    updateRules(state, action: PayloadAction<FormattingRules>) {
      return action.payload;
    },
  },
});

export const { updateRules } = rulesSlice.actions;
export default rulesSlice.reducer;