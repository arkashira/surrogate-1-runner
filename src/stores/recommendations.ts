import { defineStore } from 'pinia'
import axios from 'axios'

export interface Recommendation {
  id: number
  title: string
  description: string
  impact: 'High' | 'Medium' | 'Low'
  jobName: string
  currentValue: string
  suggestedValue: string
}

export const useRecommendationsStore = defineStore('recommendations', {
  state: () => ({
    list: [] as Recommendation[],
    loading: false,
    error: null as string | null
  }),

  getters: {
    hasRecommendations: (state) => state.list.length > 0
  },

  actions: {
    async fetch() {
      this.loading = true
      this.error = null
      try {
        const { data } = await axios.get<Recommendation[]>('/api/recommendations')
        this.list = data
      } catch (e: any) {
        this.error = e.response?.data?.message ?? 'Failed to load recommendations'
      } finally {
        this.loading = false
      }
    },

    async apply(rec: Recommendation) {
      try {
        await axios.post(`/api/recommendations/${rec.id}/apply`)
        this.list = this.list.filter(r => r.id !== rec.id)
        this.$toast.success(`Applied: ${rec.title}`)
      } catch (e: any) {
        this.$toast.error(`Could not apply: ${rec.title}`)
      }
    },

    async dismiss(rec: Recommendation) {
      try {
        await axios.post(`/api/recommendations/${rec.id}/dismiss`)
        this.list = this.list.filter(r => r.id !== rec.id)
        this.$toast.info(`Dismissed: ${rec.title}`)
      } catch (e: any) {
        this.$toast.error(`Could not dismiss: ${rec.title}`)
      }
    }
  }
})