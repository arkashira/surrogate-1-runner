import axios from 'axios'

const state = {
  costs: {
    total: 0,
    byProvider: { aws: 0, gcp: 0, azure: 0 },
    byJob: {}          // { [jobId]: { total, byProvider:{...} } }
  },
  loading: false,
  error: null,
  lastUpdated: null
}

const getters = {
  totalCost: s => s.costs.total,
  costByProvider: s => s.costs.byProvider,
  costByJob: s => jobId => s.costs.byJob[jobId] || null,
  isLoading: s => s.loading,
  costError: s => s.error,
  lastUpdated: s => s.lastUpdated
}

const mutations = {
  SET_COSTS (s, payload) {
    s.costs = payload
    s.lastUpdated = new Date().toISOString()
  },
  SET_LOADING (s, flag) { s.loading = flag },
  SET_ERROR (s, err)   { s.error = err },
  UPDATE_JOB_COST (s, { jobId, cost, provider }) {
    const job = s.costs.byJob[jobId] ?? { total: 0, byProvider: {} }
    job.total += cost
    job.byProvider[provider] = (job.byProvider[provider] ?? 0) + cost
    s.costs.byJob[jobId] = job

    s.costs.total += cost
    s.costs.byProvider[provider] = (s.costs.byProvider[provider] ?? 0) + cost
  }
}

const actions = {
  async fetchCosts ({ commit }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const { data } = await axios.get('/api/costs')
      commit('SET_COSTS', data)
    } catch (e) {
      commit('SET_ERROR', e.message || 'Failed to fetch costs')
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchJobCost ({ commit }, jobId) {
    try {
      const { data } = await axios.get(`/api/costs/job/${jobId}`)
      const { cost, provider } = data
      commit('UPDATE_JOB_COST', { jobId, cost, provider })
    } catch (e) {
      commit('SET_ERROR', e.message || 'Failed to fetch job cost')
    }
  },

  startCostPolling ({ dispatch }, intervalMs = 30_000) {
    dispatch('fetchCosts')
    setInterval(() => dispatch('fetchCosts'), intervalMs)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}