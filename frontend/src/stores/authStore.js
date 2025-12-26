import { defineStore } from 'pinia'
import api from '@/api/axios'
import router from '@/router'

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    role: null,
    token: null
  }),

  actions: {
    async login(email, password) {
      try {
        const res = await api.post("/auth/login", { email, password })

        this.user = res.data.data
        this.role = res.data.data.role || "user"
        this.token = null

        if (this.role === "admin") {
          router.push("/admin/dashboard")
        } else {
          router.push("/user/dashboard")
        }
      } catch (error) {
        alert(error.response?.data?.message || "Login failed")
      }
    },

    async register(name, email, password) {
      try {
        await api.post("/auth/register", { name, email, password })
        router.push("/")
      } catch (error) {
        alert("Registration failed")
      }
    },

    logout() {
      this.user = null
      this.role = null
      this.token = null
      router.push("/")
    }
  }
})
