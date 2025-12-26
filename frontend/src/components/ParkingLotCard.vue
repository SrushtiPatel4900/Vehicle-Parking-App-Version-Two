<template>
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body">

        <!-- Lot Title -->
        <h5 class="card-title">{{ lot.prime_location_name }}</h5>

        <!-- Location / Address -->
        <p><strong>Location:</strong> {{ lot.address }}</p>

        <!-- Available Spots -->
        <p>
          <strong>Spots:</strong>
          {{ lot.number_of_spots }}
        </p>

        <button class="btn btn-primary w-100" @click="$emit('open-spots', lot.id)">
          View Spots
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(["lot"])
</script>
