<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h3 class="text-center mb-3">Login</h3>

    <div class="card p-3">
      <input v-model="email" class="form-control mb-3" type="email" placeholder="Email">
      <input v-model="password" class="form-control mb-3" type="password" placeholder="Password">

      <button @click="login" class="btn btn-primary w-100">Login</button>

      <p class="mt-3 text-center">
        <router-link to="/register">Create an account</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/authStore"

const email = ref("")
const password = ref("")

const auth = useAuthStore()

const login = () => {
  auth.login(email.value, password.value)
}
</script>
