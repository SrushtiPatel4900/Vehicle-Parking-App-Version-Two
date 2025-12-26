<!-- src/views/AdminDashboard.vue -->
<template>
  <div>
    <!--<AdminNavbar />-->
    <div class="container mt-4">
      <h3>Admin Dashboard</h3>

      <div class="row g-3 mt-3">
        <div class="col-md-3" v-for="(val, key) in summaryCards" :key="key">
          <div class="card p-3">
            <div class="h5">{{ val.title }}</div>
            <div class="display-6">{{ val.value }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import { onMounted, reactive } from 'vue'
import { useAdminStore } from '@/stores/adminStore'

const admin = useAdminStore()

const summaryCards = reactive({
  lots: { title: 'Total Lots', value: 0 },
  spots: { title: 'Total Spots', value: 0 },
  occupied: { title: 'Occupied Spots', value: 0 },
  users: { title: 'Users', value: 0 }
})

onMounted(async () => {
  await admin.fetchLots()
  await admin.fetchUsers()
  await admin.fetchBookings()
  // compute summary
  summaryCards.lots.value = admin.lots.length
  summaryCards.users.value = admin.users.length
  summaryCards.spots.value = admin.lots.reduce((acc, l) => acc + (l.number_of_spots || 0), 0)
  summaryCards.occupied.value = admin.bookings.filter(b => !b.leaving_timestamp).length
})
</script>
