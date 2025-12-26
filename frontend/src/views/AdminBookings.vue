<!-- src/views/AdminBookings.vue -->
<template>
  <div>
    <!--<AdminNavbar />-->
    <div class="container mt-4">
      <h3>All Bookings</h3>

      <div v-if="loading" class="text-center">Loading...</div>

      <div v-else>
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>User ID</th>
              <th>Prime Location</th>
              <th>Spot ID</th>
              <th>Vehicle</th>
              <th>Start</th>
              <th>End</th>
              <th>Cost</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings" :key="b.id">
              <td>{{ b.id }}</td>
              <td>{{ b.user_id }}</td>
               <td>{{ b.lot_name ?? '-' }}</td>
              <td>{{ b.spot_id }}</td>
              <td>{{ b.vehicle_number }}</td>
              <td>{{ fmt(b.parking_timestamp) }}</td>
              <td>{{ fmt(b.leaving_timestamp) }}</td>
              <td>{{ b.parking_cost ?? '-' }}</td>
              <td>
                <button v-if="!b.leaving_timestamp" class="btn btn-sm btn-danger" @click="finalize(b.id)">Finalize</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import { useAdminStore } from '@/stores/adminStore'
import { onMounted } from 'vue'

const admin = useAdminStore()
const bookings = admin.bookings
const loading = admin.loading

onMounted(() => admin.fetchBookings())

async function finalize(id) {
  if (!confirm('Finalize this booking and release spot?')) return
  const res = await admin.finalizeBooking(id)
  alert(res.message || 'Finalized')
  admin.fetchBookings()
}

function fmt(ts) {
  if (!ts) return '-'
  return new Date(ts).toLocaleString()
}
</script>


