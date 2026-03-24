<template>
  <div class="chart-wrapper">
    <Line v-if="data && data.labels && data.labels.length" :data="chartData" :options="chartOptions" />
    <div v-else>No data available to plot on the chart.</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const colors = [
  '#f87979', '#42b983', '#3498db', '#9b59b6', '#f1c40f',
  '#e67e22', '#e74c3c', '#95a5a6', '#34495e', '#16a085'
]

const chartData = computed(() => ({
  labels: props.data.labels || [],
  datasets: (props.data.datasets || []).map((ds, index) => ({
    ...ds,
    backgroundColor: colors[index % colors.length],
    borderColor: colors[index % colors.length],
    tension: 0.1
  }))
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false,
      title: {
        display: true,
        text: 'Price (€)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Time (Year-Month)'
      }
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
  height: 400px;
  position: relative;
}
</style>
