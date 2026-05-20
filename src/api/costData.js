
import axios from 'axios'

export default {
  async fetchCostData() {
    const response = await axios.get('/api/costs')
    return response.data
  }
}