<template>
  <div id="app">
    <header>
      <h1>Wine Monthly Average Prices Dashboard</h1>
      <button @click="fetchData">Refresh Data</button>
    </header>
    <main>
      <div v-if="loading">Loading data...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else>
        <section class="controls">
           <label for="country-selector">Select Country for Graph: </label>
           <select id="country-selector" v-model="selectedCountry">
             <option value="">All Countries (Average)</option>
             <option v-for="country in countries" :key="country" :value="country">
               {{ country }}
             </option>
           </select>
        </section>

        <section class="visuals">
          <div class="chart-container">
            <h2>Price Trends</h2>
            <DataChart :data="filteredData" />
          </div>
          <div class="table-container">
            <h2>Data Table</h2>
            <DataTable :data="filteredTableData" />
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import DataTable from './components/DataTable.vue'
import DataChart from './components/DataChart.vue'

const prices = ref([])
const loading = ref(true)
const error = ref(null)
const selectedCountry = ref('')

// Get repository URL from environment, or use default
const repositoryUrl = import.meta.env.VITE_REPOSITORY_URL || 'http://localhost:8000'

const fetchData = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get(`${repositoryUrl}/prices/averages`)
    prices.value = response.data
  } catch (err) {
    console.error('Error fetching data:', err)
    error.value = 'Failed to load data from repository service.'
  } finally {
    loading.value = false
  }
}

const countries = computed(() => {
  const set = new Set(prices.value.map(p => p.member_state_name))
  return Array.from(set).sort()
})

const filteredData = computed(() => {
  if (!selectedCountry.value) {
    // If no country selected, aggregate all prices by month
    const aggregated = {}
    prices.value.forEach(p => {
      const key = `${p.year}-${String(p.month).padStart(2, '0')}`
      if (!aggregated[key]) aggregated[key] = { count: 0, sum: 0 }
      aggregated[key].sum += p.avg_price_value
      aggregated[key].count += 1
    })
    const sortedKeys = Object.keys(aggregated).sort()
    return {
      labels: sortedKeys,
      datasets: [{
        label: 'Average Price (€) - All Countries',
        data: sortedKeys.map(key => (aggregated[key].sum / aggregated[key].count))
      }]
    }
  }

  // Filter by country
  const countryPrices = prices.value.filter(p => p.member_state_name === selectedCountry.value)

  // Find all unique months (labels)
  const labels = Array.from(new Set(countryPrices.map(p => `${p.year}-${String(p.month).padStart(2, '0')}`))).sort()

  // Find all unique descriptions
  const descriptions = Array.from(new Set(countryPrices.map(p => p.description))).sort()

  // Create datasets for each description
  const datasets = descriptions.map(desc => {
    return {
      label: desc,
      data: labels.map(label => {
        const p = countryPrices.find(p => `${p.year}-${String(p.month).padStart(2, '0')}` === label && p.description === desc)
        return p ? p.avg_price_value : null
      })
    }
  })

  return { labels, datasets }
})

const filteredTableData = computed(() => {
  let data = prices.value
  if (selectedCountry.value) {
    data = data.filter(p => p.member_state_name === selectedCountry.value)
  }

  return [...data].sort((a, b) => {
    const descComp = a.description.localeCompare(b.description)
    if (descComp !== 0) return descComp
    if (a.year !== b.year) return a.year - b.year
    return a.month - b.month
  })
})

onMounted(fetchData)
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background-color: #f4f4f4;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #ddd;
  margin-bottom: 20px;
}
.error {
  color: red;
  font-weight: bold;
}
.controls {
  margin-bottom: 20px;
}
.visuals {
  display: flex;
  flex-direction: column;
  gap: 40px;
}
.chart-container, .table-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
h2 {
  margin-top: 0;
}
</style>
