<template>
  <div class="table-wrapper">
    <table v-if="data.length">
      <thead>
        <tr>
          <th>Country</th>
          <th>Description</th>
          <th>Year</th>
          <th>Month</th>
          <th>Avg Price (€)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in data" :key="index">
          <td>{{ item.member_state_name }}</td>
          <td>{{ item.description }}</td>
          <td>{{ item.year }}</td>
          <td>{{ item.month }}</td>
          <td>{{ item.avg_price_value.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>No data available to display in the table.</div>
  </div>
</template>

<script setup>
defineProps({
  data: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.table-wrapper {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #eee;
}
th {
  background-color: #f8f9fa;
  font-weight: bold;
}
tr:hover {
  background-color: #f1f1f1;
}
</style>
