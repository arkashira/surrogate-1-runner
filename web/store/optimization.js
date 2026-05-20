const state = {
  optimizationRecommendations: [],
};

const mutations = {
  SET_OPTIMIZATION_RECOMMENDATIONS(state, recommendations) {
    state.optimizationRecommendations = recommendations;
  },
};

const actions = {
  async fetchOptimizationSuggestions({ commit }) {
    // Simulate fetching optimization data
    const recommendations = [
      'Replace GPT-3.5 with Claude-2 for cost savings',
      'Batch process similar requests for efficiency',
      'Consider using free tier models for underutilized tasks',
    ];

    commit('SET_OPTIMIZATION_RECOMMENDATIONS', recommendations);
  },
};

const getters = {
  optimizationRecommendations: state => state.optimizationRecommendations,
};

export default {
  state,
  mutations,
  actions,
  getters,
};