<script setup>
import { ref, onMounted } from "vue";
import axios from "@/api/axios";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

// Refs for both charts
const lotChartRef = ref(null);
const occupancyChartRef = ref(null);

// Store chart instances (for HMR / re-render safety)
let lotChart = null;
let occupancyChart = null;

const chartData = ref({
  spots_by_lot: []
});

// Fetch API data
const fetchCharts = async () => {
  try {
    const res = await axios.get("/chart/admin");
    chartData.value = res.data.data;
    renderCharts();
  } catch (err) {
    console.error("Chart error:", err);
  }
};

const renderCharts = () => {
  const lots = chartData.value.spots_by_lot;

  const labels = lots.map(l => l.lot_name);
  const occupied = lots.map(l => l.occupied);
  const available = lots.map(l => l.available);

  const occupancyPercent = lots.map(l =>
    l.total_spots === 0 ? 0 : Math.round((l.occupied / l.total_spots) * 100)
  );

  // ---------------------------------------
  // GRAPH 1 - STACKED BAR (Available vs Occupied)
  // ---------------------------------------
  if (lotChart) lotChart.destroy();
  lotChart = new Chart(lotChartRef.value, {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Occupied", data: occupied, backgroundColor: "#f871efff" },
        { label: "Available", data: available, backgroundColor: "#4aded2ff" }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: "Parking Lot Summary" }
      },
      scales: {
        x: { stacked: true },
        y: { stacked: true, beginAtZero: true }
      }
    }
  });

  // ---------------------------------------
  // GRAPH 2 - OCCUPANCY RATE (% Horizontal Bar)
  // ---------------------------------------
  if (occupancyChart) occupancyChart.destroy();
  occupancyChart = new Chart(occupancyChartRef.value, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Occupancy Rate (%)",
          data: occupancyPercent,
          backgroundColor: "rgba(99, 102, 241, 0.6)",
          borderColor: "rgba(99, 102, 241, 1)",
          borderWidth: 1
        }
      ]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      plugins: {
        title: { display: true, text: "Occupancy Rate per Lot (%)" }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          title: { display: true, text: "Percentage (%)" }
        }
      }
    }
  });
};

onMounted(fetchCharts);
</script>

<template>
  <div class="container mt-3">

    <h2>Admin Analytics Dashboard</h2>

    <!-- GRAPH 1: STACKED BAR -->
    <div class="card p-3 my-4">
      <h5>Parking Lot Status (Available vs Occupied)</h5>
      <canvas ref="lotChartRef"></canvas>
    </div>

    <!-- GRAPH 2: OCCUPANCY RATE (%) -->
    <div class="card p-3 my-4">
      <h5>Occupancy Rate (%) per Parking Lot</h5>
      <canvas ref="occupancyChartRef"></canvas>
    </div>

  </div>
</template>

<style>
.card {
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>


