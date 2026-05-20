import { Module } from 'vuex';
import axios from 'axios';
import { RootState } from '../index';

export interface AlertSettings {
  costThreshold: number | null;
  lookbackPeriod: '1h' | '24h' | '7d' | '30d';
  emailEnabled: boolean;
  emailRecipients: string;   // comma‑separated
  slackEnabled: boolean;
  slackWebhookUrl: string;
}

export interface AlertsState {
  settings: AlertSettings;
  loading: boolean;
  error: string | null;
}

const state: AlertsState = {
  settings: {
    costThreshold: null,
    lookbackPeriod: '24h',
    emailEnabled: false,
    emailRecipients: '',
    slackEnabled: false,
    slackWebhookUrl: '',
  },
  loading: false,
  error: null,
};

const getters = {
  alertSettings: (s: AlertsState) => s.settings,
  isLoading: (s: AlertsState) => s.loading,
  errorMessage: (s: AlertsState) => s.error,
};

const actions = {
  async fetchAlertSettings({ commit }: any) {
    commit('SET_LOADING', true);
    try {
      const { data } = await axios.get<AlertSettings>('/api/alerts/settings');
      commit('SET_SETTINGS', data);
      commit('SET_ERROR', null);
    } catch (e) {
      commit('SET_ERROR', 'Failed to load alert settings.');
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async saveAlertSettings({ commit }: any, payload: AlertSettings) {
    commit('SET_LOADING', true);
    try {
      await axios.post('/api/alerts/settings', payload);
      commit('SET_SETTINGS', payload);
      commit('SET_ERROR', null);
    } catch (e) {
      commit('SET_ERROR', 'Failed to save alert settings.');
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async sendTestAlert({ state }: any) {
    try {
      await axios.post('/api/alerts/test', { settings: state.settings });
    } catch (e) {
      // The component will handle the UI error
      throw new Error('Test alert failed');
    }
  },
};

const mutations = {
  SET_SETTINGS(s: AlertsState, payload: AlertSettings) {
    s.settings = payload;
  },
  SET_LOADING(s: AlertsState, flag: boolean) {
    s.loading = flag;
  },
  SET_ERROR(s: AlertsState, msg: string | null) {
    s.error = msg;
  },
};

export const alerts: Module<AlertsState, RootState> = {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};