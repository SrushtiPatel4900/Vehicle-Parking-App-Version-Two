<script setup>
import { ref, onMounted } from "vue";
import axios from "@/api/axios";
import { useAuthStore } from "@/stores/authStore";      // adjust if needed
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

// Store
const store = useAuthStore();
const userId = store.user.id;

// Refs for chart elements
const usageChartRef = ref(null);
const pieChartRef = ref(null);

// Data from backend
const chartData = ref({
  spots_by_lot: []
});

// Fetch data
const fetchCharts = async () => {
  try {
    const res = await axios.get("/chart/user-dashboard", {
      params: { user_id: userId }
    });

    chartData.value = res.data.data;
    renderCharts();

  } catch (err) {
    console.error("Chart error:", err);
  }
};

// Render the charts after data is fetched
const renderCharts = () => {
  const labels = chartData.value.spots_by_lot.map(l => l.lot_name);
  const occupied = chartData.value.spots_by_lot.map(l => l.user_booked || 0);
  const available = chartData.value.spots_by_lot.map(
    l => l.total_spots - (l.user_booked || 0)
  );

  // Destroy previous charts
  if (usageChartRef.value?.chart) usageChartRef.value.chart.destroy();
  if (pieChartRef.value?.chart) pieChartRef.value.chart.destroy();

  // 1) Stacked Bar Chart
  usageChartRef.value.chart = new Chart(usageChartRef.value, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Occupied by Me",
          data: occupied,
          backgroundColor: "rgba(54, 162, 235, 0.7)"
        },
        {
          label: "Available",
          data: available,
          backgroundColor: "rgba(75, 192, 192, 0.7)"
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: "My Parking Usage Summary" }
      },
      scales: {
        x: { stacked: true },
        y: { stacked: true, beginAtZero: true }
      }
    }
  });

  // 2) Pie Chart
  const totalUserBooked = occupied.reduce((a, b) => a + b, 0);
  const totalAvailable = available.reduce((a, b) => a + b, 0);

  pieChartRef.value.chart = new Chart(pieChartRef.value, {
    type: "pie",
    data: {
      labels: ["My Booked Spots", "Remaining Spots"],
      datasets: [
        {
          data: [totalUserBooked, totalAvailable],
          backgroundColor: [
            "rgba(54, 162, 235, 0.7)",
            "rgba(75, 192, 192, 0.7)"
          ]
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: "My Parking Spot Proportion" }
      }
    }
  });
};

onMounted(fetchCharts);
</script>

<template>
  <div class="container mt-3">
    
    <h2>User Parking Analytics</h2>

    <!-- Stacked Bar Chart -->
    <div class="card p-3 my-4">
      <h5>My Parking Usage Summary</h5>
      <canvas ref="usageChartRef"></canvas>
    </div>

    <!-- Pie Chart -->
    <div class="card p-3 my-4">
      <h5>My Spot Proportion</h5>
      <canvas ref="pieChartRef"></canvas>
    </div>

  </div>
</template>

<style>
.card {
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>

