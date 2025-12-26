<!-- src/components/AdminLotCard.vue -->
<template>
  <div class="card h-100">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ lot.prime_location_name }}</h5>
      <p class="mb-1 small-muted">{{ lot.address }} • {{ lot.pin_code }}</p>
      <p class="mb-2">Price/hr: ₹{{ lot.price_per_hour }}</p>
      <div class="mt-auto d-flex justify-content-end">
        <button class="btn btn-sm btn-outline-primary me-1" @click="$emit('edit', lot)">Edit</button>
        <button class="btn btn-sm btn-outline-secondary me-1" @click="$emit('manage', lot)">Manage Spots</button>
        <button class="btn btn-sm btn-danger" @click="$emit('delete', lot.id)">Delete</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ lot: Object })
</script>

<style scoped>
.small-muted { color: #6c757d; font-size: 0.9rem; }
</style>
