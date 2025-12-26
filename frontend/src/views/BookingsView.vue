<template>
  <div class="container mt-4">
    <h2 class="mb-3">My Bookings</h2>

    <div class="row g-3">
      <BookingCard
        v-for="b in bookings"
        :key="b.id"
        :booking="b"
        @release="releaseBooking"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/api/axios"
import BookingCard from "@/components/BookingCard.vue"
import { useAuthStore } from "@/stores/authStore"

const bookings = ref([])
const auth = useAuthStore()
const fetchBookings = async () => {
  if (!auth.user) return
  const res = await api.get(`/bookings/user?user_id=${auth.user.id}`)
  bookings.value = res.data.data.bookings || []
}

onMounted(() => {
  fetchBookings()
})

const releaseBooking = async (id) => {
  if (!confirm("Release this booking?")) return;

  const res = await api.post(`/bookings/release/${id}`);

  alert(`Released! Total Cost = ₹${res.data.data.parking_cost}`);

  fetchBookings();
};


</script>


