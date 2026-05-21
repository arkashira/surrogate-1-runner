import { create } from 'zustand'

interface SettingsState {
  syncEnabled: boolean
  setSyncEnabled: (enabled: boolean) => void
}

export const useSettingsStore = create<SettingsState>((set) => ({
  syncEnabled: localStorage.getItem('syncEnabled') === 'true' || false,
  setSyncEnabled: (enabled) => {
    localStorage.setItem('syncEnabled', String(enabled))
    set({ syncEnabled: enabled })
  }
}))