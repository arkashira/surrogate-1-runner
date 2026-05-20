<template>
  <div class="price-chart">
    <div class="chart-header">
      <h3 v-if="title">{{ title }}</h3>
      <button @click="exportCsv" class="export-btn">Export CSV</button>
    </div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue';
import { Chart, registerables, ChartData, ChartOptions } from 'chart.js';

Chart.register(...registerables);

type Point = { price: number; quantity: number; elasticity: number };

const props = defineProps<{
  /** Array of data points: { price, quantity, elasticity } */
  points: Point[];
  /** Optional chart title */
  title?: string;
}>();

const emits = defineEmits<{
  /** Emitted when a point is clicked */
  (e: 'point-click', point: Point): void;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

// ------------------------------------------------------------------
// Chart creation
// ------------------------------------------------------------------
const createChart = () => {
  if (!chartCanvas.value) return;

  const data: ChartData<'line'> = {
    labels: props.points.map(p => p.price.toFixed(2)),
    datasets: [
      {
        label: 'Elasticity',
        data: props.points.map(p => p.elasticity),
        borderColor: '#42b983',
        backgroundColor: 'rgba(66,185,131,0.2)',
        fill: true,
        tension: 0.4,
        pointRadius: 5,
        pointHoverRadius: 7,
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: !!props.title,
        text: props.title,
        font: { size: 18 },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const idx = context.dataIndex;
            const point = props.points[idx];
            return [
              `Price: $${point.price.toFixed(2)}`,
              `Quantity: ${point.quantity}`,
              `Elasticity: ${point.elasticity.toFixed(3)}`,
            ];
          },
        },
      },
      legend: { display: false },
    },
    scales: {
      x: {
        title: { display: true, text: 'Price ($)' },
        ticks: { callback: (value) => value?.toString() },
      },
      y: {
        title: { display: true, text: 'Elasticity' },
        beginAtZero: false,
      },
    },
    onClick: (evt, elements) => {
      if (elements.length > 0) {
        const idx = elements[0].index;
        emits('point-click', props.points[idx]);
      }
    },
  };

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data,
    options,
  });
};

// ------------------------------------------------------------------
// Chart update
// ------------------------------------------------------------------
const updateChart = () => {
  if (!chartInstance) return;
  chartInstance.data.labels = props.points.map(p => p.price.toFixed(2));
  chartInstance.data.datasets[0].data = props.points.map(p => p.elasticity);
  chartInstance.update();
};

// ------------------------------------------------------------------
// CSV export
// ------------------------------------------------------------------
const exportCsv = () => {
  const header = 'Price,Quantity,Elasticity\n';
  const rows = props.points
    .map(p => `${p.price.toFixed(2)},${p.quantity},${p.elasticity.toFixed(6)}`)
    .join('\n');
  const csvContent = header + rows;
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'price_elasticity.csv';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

// ------------------------------------------------------------------
// Lifecycle hooks
// ------------------------------------------------------------------
onMounted(() => {
  createChart();
});

watch(
  () => props.points,
  () => {
    updateChart();
  },
  { deep: true }
);
</script>

<style scoped>
.price-chart {
  position: relative;
  width: 100%;
  height: 420px;
  padding: 1rem;
  box-sizing: border-box;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.export-btn {
  background: #42b983;
  color: #fff;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
}
.export-btn:hover {
  background: #369a6e;
}
</style>