<!-- src/views/AdminLots.vue -->
<template>
  <div>
    <!--<AdminNavbar />-->
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>Parking Lots</h3>
        <button class="btn btn-success" @click="openCreate">+ Add Lot</button>
      </div>

      <div v-if="loading" class="text-center">Loading...</div>

      <div v-else>
        <div v-if="lots.length === 0" class="alert alert-info">No parking lots found.</div>

        <div class="row g-3">
          <div class="col-md-4" v-for="lot in lots" :key="lot.id">
            <AdminLotCard :lot="lot" @edit="startEdit" @delete="remove" @manage="manageSpots" />
          </div>
        </div>
      </div>

      <!-- Create / Edit panel -->
      <div v-if="showForm" class="mt-4">
        <AdminLotForm :initial="editing" @save="save" @cancel="closeForm" />
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminLotCard from '@/components/AdminLotCard.vue'
import AdminLotForm from '@/components/AdminLotForm.vue'
import { ref, onMounted } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useRouter } from 'vue-router'

const admin = useAdminStore()
const router = useRouter()
const showForm = ref(false)
const editing = ref(null)
const loading = ref(false)

async function load() {
  loading.value = true
  await admin.fetchLots()
  loading.value = false
}

onMounted(load)

function openCreate() {
  editing.value = {}
  showForm.value = true
}

function startEdit(lot) {
  editing.value = { ...lot }
  showForm.value = true
}

async function save(payload) {
  if (payload.id) {
    const res = await admin.updateLot(payload.id, payload)
    alert(res.message || 'Updated')
  } else {
    const res = await admin.createLot(payload)
    alert(res.message || 'Created')
  }
  showForm.value = false
  await load()
}

async function remove(id) {
  if (!confirm('Delete this lot? Only allowed if all spots are empty.')) return
  const res = await admin.deleteLot(id)
  alert(res.message || 'Deleted')
  await load()
}


function manageSpots(lot) {
  router.push(`/admin/spots/${lot.id}`);
}

const lots = admin.lots
</script>
