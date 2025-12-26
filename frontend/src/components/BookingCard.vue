<template>
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5>Lot: {{ booking.lot_name }}</h5>
        <p>Spot: {{ booking.spot_number }}</p>
        <p>Status: <strong>{{ booking.status }}</strong></p>

        <p v-if="booking.status === 'released'">
          <strong>Cost:</strong> ₹{{ booking.cost }}
        </p>

        <button
          v-if="booking.status === 'active'"
          class="btn btn-danger w-100"
          @click="$emit('release', booking.id)"
        >
          Release
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(["booking"])
</script>
