<!-- src/views/AdminUsers.vue -->
<template>
  <div>
    <!--<AdminNavbar />-->
    <div class="container mt-4">
      <h3>Registered Users</h3>

      <div v-if="loading" class="text-center">Loading...</div>

      <div v-else>
        <table class="table table-striped">
          <thead>
            <tr><th>ID</th><th>Username</th><th>Email</th><th>Created</th></tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.username ?? u.name ?? '-' }}</td>
              <td>{{ u.email }}</td>
              <td>{{ format(u.created_at) }}</td>
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
const users = admin.users
const loading = admin.loading

onMounted(() => admin.fetchUsers())

function format(ts) {
  if (!ts) return '-'
  return new Date(ts).toLocaleString()
}
</script>
