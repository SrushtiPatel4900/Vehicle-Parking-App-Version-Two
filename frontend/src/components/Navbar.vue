<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
    <a class="navbar-brand" href="#">Parking System</a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navContent">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navContent">
      <!-- PUBLIC (non-logged in) -->
      <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="!auth.user">
        <li class="nav-item"><router-link class="nav-link" to="/">Login</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/register">Register</router-link></li>
      </ul>

      <!-- USER NAV -->
      <ul class="navbar-nav me-auto" v-if="auth.role === 'user'">
        <li class="nav-item"><router-link class="nav-link" to="/user/dashboard">Dashboard</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/user/lots">Parking Lots</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/user/bookings">My Bookings</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/user/charts">Charts</router-link></li>
      </ul>

      <!-- ADMIN NAV -->
      <ul class="navbar-nav me-auto" v-if="auth.role === 'admin'">
        <li class="nav-item"><router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/admin/lots">Parking Lots</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/admin/users">Users</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/admin/bookings">Bookings</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/admin/charts">Charts</router-link></li>
      </ul>

      <!-- RIGHT SIDE -->
      <ul class="navbar-nav ms-auto" v-if="auth.user">
        <li class="nav-item">
          <button class="btn btn-danger btn-sm" @click="auth.logout()">Logout</button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from "@/stores/authStore"
const auth = useAuthStore()
</script>
