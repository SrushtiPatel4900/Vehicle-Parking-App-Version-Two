<!-- src/components/AdminNavbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/admin/dashboard">Admin Panel</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#adminNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="adminNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link" to="/admin/lots">Lots</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/users">Users</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/bookings">Bookings</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/charts">Charts</router-link></li>
        </ul>

        <div class="d-flex">
          <button class="btn btn-outline-light me-2" @click="openFrontend">Frontend</button>
          <button class="btn btn-outline-light" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function logout(){
  localStorage.removeItem('vpa_token')
  localStorage.removeItem('vpa_user')
  router.push('/login')
}
function openFrontend(){
  window.location.href = '/'
}
</script>

<style scoped>
.navbar-brand { font-weight: 700; }
</style>
