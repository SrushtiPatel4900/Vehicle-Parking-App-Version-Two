<template>
  <div class="container mt-4">
    <h3>Parking Spots</h3>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border"></div>
    </div>

    <div v-else-if="!lot" class="alert alert-warning">
      Parking lot not found.
    </div>

    <div v-else>
      <h5>{{ lot.prime_location_name }}</h5>

      <div class="row mt-3">
        <SpotCard
          v-for="s in spots"
          :key="s.id"
          :spot="s"
          :isAdmin="true"
          @viewDetails="loadSpotDetails"
        />
      </div>
    </div>

    <!-- Spot Details Modal -->
    <div class="modal fade show" v-if="showModal" style="display:block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5>Spot Details</h5>
            <button class="btn-close" @click="showModal=false"></button>
          </div>

          <div class="modal-body" v-if="spotDetails">
            <p><strong>User:</strong> {{ spotDetails.user.name }}</p>
            <p><strong>Email:</strong> {{ spotDetails.user.email }}</p>
            <p><strong>Vehicle:</strong> {{ spotDetails.vehicle_number }}</p>
            <p><strong>Start:</strong> {{ new Date(spotDetails.start_time).toLocaleString() }}</p>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal=false">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, computed, ref } from "vue"
import { useRoute } from "vue-router"
import { useAdminStore } from "@/stores/adminStore"
import SpotCard from "@/components/SpotCard.vue"
import axios from "@/api/axios"

const route = useRoute()
const admin = useAdminStore()

const lotId = route.params.lotId
const loading = ref(true)

const lot = computed(() =>
  admin.lots.find(l => String(l.id) === String(lotId))
)

const spots = ref([]) // ⬅ FIXED: we store spots here

const showModal = ref(false)
const spotDetails = ref(null)

onMounted(async () => {
  // first load lots so lot name displays
  await admin.fetchLots()

  // now load spots separately
  const res = await axios.get(`/lots/${lotId}/spots`)
  spots.value = res.data.data.spots

  loading.value = false
})

async function loadSpotDetails(id) {
  const res = await axios.get(`/admin/spot-details/${id}`)
  spotDetails.value = res.data.data
  showModal.value = true
}
</script>
