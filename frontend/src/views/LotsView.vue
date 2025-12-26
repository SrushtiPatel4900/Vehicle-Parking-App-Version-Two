<template>
  <div class="container mt-4">
    <h2 class="mb-3">Parking Lots</h2>

    <div class="row g-3">
      <ParkingLotCard
        v-for="lot in lots"
        :key="lot.id"
        :lot="lot"
        @open-spots="goToSpots"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/api/axios"
import ParkingLotCard from "@/components/ParkingLotCard.vue"
import router from "@/router"

const lots = ref([])

onMounted(async () => {
  const res = await api.get("/lots")
  lots.value = res.data.data.lots   // ✔ correct JSON structure
})

const goToSpots = (lotId) => {
  router.push(`/user/spots/${lotId}`)
}
</script>
