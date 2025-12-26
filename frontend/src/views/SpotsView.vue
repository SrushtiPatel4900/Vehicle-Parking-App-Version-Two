<template>
  <div class="container mt-4">
    <h2 class="mb-3">Parking Spots for Lot {{ lotName }}</h2>

    <div class="row g-3">
      <SpotCard
        v-for="spot in spots"
        :key="spot.id"
        :spot="spot"
        @book="bookSpot"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "@/api/axios"
import SpotCard from "@/components/SpotCard.vue"
import { useAuthStore } from "@/stores/authStore"

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const spots = ref([])
const lotName = ref("")

onMounted(async () => {
  const lotId = route.params.lotId

  const res = await api.get(`/lots/${lotId}/spots`)
  spots.value = res.data.data.spots
  lotName.value = res.data.data.lot_name
})

const bookSpot = async () => {
  if (!confirm("Book this parking spot?")) return;

  const lotId = route.params.lotId;

  const res = await api.post(`/reserve`, {
    user_id: auth.user.id,
    lot_id: lotId,
    vehicle_number: "GJ05AB1234"  // Later replace with user input
  });

  alert("Booking Successful!");
  router.push("/user/bookings");
};

</script>
