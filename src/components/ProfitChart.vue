<template>
  <div class="profit-chart" ref="chartContainer">
    <canvas ref="chartCanvas"></canvas>

    <!-- Simple fallback UI – can be replaced with a spinner / error component -->
    <div v-if="loading" class="status">Loading…</div>
    <div v-else-if="error" class="status error">{{ error }}</div>
    <div v-else-if="!hasData" class="status">No data available.</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import axios from 'axios'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  CategoryScale,
  Legend,
} from 'chart.js'

// Register only what we need – keeps the bundle lean
Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  CategoryScale,
  Legend
)

interface ProfitRecord {
  date: string          // YYYY‑MM‑DD
  netProfit: number
}

const chartContainer = ref<HTMLElement | null>(null)
const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

const loading = ref(true)
const error = ref<string | null>(null)
const hasData = ref(false)

// ---------------------------------------------------------------------------
// Data fetching
// ---------------------------------------------------------------------------

/**
 * Fetches the last 30 days of net‑profit metrics.
 * Uses a 100 ms timeout to satisfy the latency requirement.
 * Returns an array of ProfitRecord or throws on error.
 */
export async function fetchData(): Promise<ProfitRecord[]> {
  const start = performance.now()
  try {
    const response = await axios.get<ProfitRecord[]>('/api/v1/finance/metrics/daily', {
      params: { range: 30 },
      timeout: 100, // 100 ms timeout
    })
    const latency = performance.now() - start
    console.log(`ProfitChart fetch latency: ${latency.toFixed(2)} ms`)

    if (!Array.isArray(response.data)) {
      throw new Error('Unexpected response format')
    }
    return response.data
  } catch (e: any) {
    console.error('ProfitChart fetch error', e)
    throw e
  }
}

// ---------------------------------------------------------------------------
// Chart creation
// ---------------------------------------------------------------------------

function createChart(data: ProfitRecord[]) {
  if (!chartCanvas.value) return

  const labels = data.map(d => d.date)
  const values = data.map(d => d.netProfit)

  const ctx = chartCanvas.value.getContext('2d')
  if (!ctx) return

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Net Profit',
          data: values,
          borderColor: '#42b983',
          backgroundColor: 'rgba(66,185,131,0.15)',
          fill: true,
          tension: 0.2,
          pointRadius: 3,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        tooltip: {
          callbacks: {
            title: ctx => `Date: ${ctx[0].label}`,
            label: ctx => `Net Profit: $${ctx.parsed.y.toLocaleString()}`,
          },
        },
        legend: { display: false },
        title: {
          display: true,
          text: 'Net Profit – Last 30 Days',
        },
      },
      scales: {
        x: {
          title: { display: true, text: 'Date' },
        },
        y: {
          title: { display: true, text: 'Net Profit ($)' },
          ticks: {
            callback: value => `$${value.toLocaleString()}`,
          },
        },
      },
    },
  })
}

// ---------------------------------------------------------------------------
// Lifecycle
// ---------------------------------------------------------------------------

async function loadAndRender() {
  try {
    const data = await fetchData()
    hasData.value = data.length > 0
    if (hasData.value) {
      await nextTick() // ensure canvas is rendered
      createChart(data)
    }
  } catch (e: any) {
    error.value = 'Failed to load profit data'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAndRender()
})

onBeforeUnmount(() => {
  chartInstance?.destroy()
})
</script>

<style scoped>
.profit-chart {
  position: relative;
  width: 100%;
  height: 400px;
}

.status {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  color: #555;
}
.status.error {
  color: #c00;
}
</style>