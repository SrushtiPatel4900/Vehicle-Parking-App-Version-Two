// src/stores/adminStore.js
import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    lots: [],
    users: [],
    bookings: [],
    charts: {},
    loading: false,
    error: null
  }),
  actions: {
    async fetchLots() {
      this.loading = true
      try {
        const res = await api.get('/lots')
        // support both shapes: res.data.data.lots OR res.data.lots
        this.lots = res.data?.data?.lots ?? res.data?.lots ?? []
      } catch (e) {
        this.error = e
        this.lots = []
      } finally { this.loading = false }
    },

    async createLot(payload) {
      const res = await api.post('/lots', payload)
      return res.data
    },

    async updateLot(id, payload) {
      const res = await api.put(`/lots/${id}`, payload)
      return res.data
    },

    async deleteLot(id) {
      const res = await api.delete(`/lots/${id}`)
      return res.data
    },

    async fetchUsers() {
      this.loading = true
      try {
        const res = await api.get('/users')
        this.users = res.data?.data?.users ?? res.data?.users ?? []
      } catch (e) {
        this.error = e
        this.users = []
      } finally { this.loading = false }
    },

    async fetchBookings() {
      this.loading = true
      try {
        const res = await api.get('admin/bookings')
        this.bookings = res.data?.data?.bookings ?? res.data?.bookings ?? []
      } catch (e) {
        this.error = e
        this.bookings = []
      } finally { this.loading = false }
    },

    async finalizeBooking(id) {
      // your backend finalize endpoint: /release/:id
      const res = await api.post(`/bookings/release/${id}`)
      return res.data
    },

    async fetchCharts() {
      const res = await api.get('/charts')
      this.charts = res.data?.data ?? res.data ?? {}
      return this.charts
    }
  }
})
