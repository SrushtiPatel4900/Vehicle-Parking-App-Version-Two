<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h3 class="text-center mb-3">Register</h3>

    <div class="card p-3">
      <input v-model="name" class="form-control mb-3" type="text" placeholder="Full Name">
      <input v-model="email" class="form-control mb-3" type="email" placeholder="Email">
      <input v-model="password" class="form-control mb-3" type="password" placeholder="Password">

      <button @click="register" class="btn btn-success w-100">Register</button>

      <p class="mt-3 text-center">
        <router-link to="/">Back to Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/authStore"

const name = ref("")
const email = ref("")
const password = ref("")

const auth = useAuthStore()

const register = () => {
  auth.register(name.value, email.value, password.value)
}
</script>
