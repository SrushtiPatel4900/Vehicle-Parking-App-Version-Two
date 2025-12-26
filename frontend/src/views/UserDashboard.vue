<template>
  <div class="container mt-4">
    <h2 class="mb-3">Welcome, {{ auth.user?.name }}</h2>

    <div class="row g-3">
      <div class="col-md-4">
        <div class="card shadow-sm p-3">
          <h4>Total Active Bookings</h4>
          <p class="fs-3">{{ dashboard.active }}</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm p-3">
          <h4>Total Released</h4>
          <p class="fs-3">{{ dashboard.released }}</p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm p-3">
          <h4>Total Cost Paid</h4>
          <p class="fs-3">₹{{ dashboard.cost }}</p>
        </div>
      </div>
    </div>

    <!-- CSV Export Section -->
    <div class="mt-4">
      <button 
        class="btn btn-primary"
        :disabled="exporting"
        @click="exportCsv"
      >
        {{ exporting ? "Exporting..." : "Export Parking CSV" }}
      </button>

      <p v-if="message" class="mt-2 text-success">{{ message }}</p>
      <p v-if="errorMessage" class="mt-2 text-danger">{{ errorMessage }}</p>
    </div>
    

  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue"
import api from "@/api/axios"
import { useAuthStore } from "@/stores/authStore"

const auth = useAuthStore()

const dashboard = reactive({
  active: 0,
  released: 0,
  cost: 0,
})
const exporting = ref(false)
const message = ref("")
const errorMessage = ref("")
let taskId = null

const fetchDashboard = async () => {
  if (!auth.user) return

  const res = await api.get(`/bookings/user?user_id=${auth.user.id}`)
  const bookings = res.data.data.bookings || []

  dashboard.active = bookings.filter(b => !b.leaving_timestamp).length
  dashboard.released = bookings.filter(b => b.leaving_timestamp).length
  dashboard.cost = bookings
    .filter(b => b.parking_cost)
    .reduce((sum, b) => sum + b.parking_cost, 0)
    .toFixed(2)
}
const exportCsv = async () => {
  if (!auth.user) return
  exporting.value = true
  message.value = ""
  errorMessage.value = ""

  try {
    const res = await api.get(`/export-csv?user_id=${auth.user.id}`)
    if (res.data.status === "started") {
      taskId = res.data.task_id
      message.value = "CSV export started! Preparing download..."
      pollTaskStatus()
    } else {
      errorMessage.value = "Failed to start CSV export"
      exporting.value = false
    }
  } catch (err) {
    errorMessage.value = `Error: ${err.message}`
    exporting.value = false
  }
}

// Poll Celery task every 3 seconds until ready
const pollTaskStatus = async () => {
  if (!taskId) return
  try {
    const res = await api.get(`/download-csv?task_id=${taskId}`, {
      responseType: "blob"
    })

    // If response is JSON (not ready)
    if (res.data && res.data.status) {
      if (res.data.status === "pending") {
        setTimeout(pollTaskStatus, 3000)
      } else if (res.data.status === "failed") {
        errorMessage.value = res.data.message
        exporting.value = false
      }
    } else {
      // CSV ready → trigger download
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement("a")
      link.href = url
      link.setAttribute("download", `parking_export_${auth.user.id}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      exporting.value = false
      message.value = "CSV download ready!"
    }
  } catch (err) {
    setTimeout(pollTaskStatus, 3000)
  }
}

onMounted(() => {
  fetchDashboard()
})


</script>
