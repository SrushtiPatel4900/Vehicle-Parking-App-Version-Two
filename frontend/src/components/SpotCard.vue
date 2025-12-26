<!-- src/components/SpotCard.vue -->
<template>
  <div class="col-md-3">
    <div
      class="card shadow-sm"
      :class="spot.status === 'O' ? 'border-danger' : 'border-success'"
    >
      <div class="card-body text-center">
        <h5>Spot {{ spot.spot_number }}</h5>
        <p>Status: <strong>{{ spot.status }}</strong></p>

        <!-- USER (Available Spot) -->
        <button
          v-if="!isAdmin && spot.status === 'A'"
          class="btn btn-primary"
          @click="$emit('book', spot.id)"
        >
          Book
        </button>

        <!-- ADMIN (View Details Only When Occupied) -->
        <button
          v-if="isAdmin && spot.status === 'O'"
          class="btn btn-danger"
          @click="$emit('viewDetails', spot.id)"
        >
          View Details
        </button>

        <!-- NOTHING for the user when occupied -->
        <div v-if="!isAdmin && spot.status === 'O'" style="height: 38px;"></div>

        <!-- NOTHING for Admin on available -->
        <div v-if="isAdmin && spot.status === 'A'" style="height: 38px;"></div>

      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  spot: Object,
  isAdmin: { type: Boolean, default: false }
})
</script>
