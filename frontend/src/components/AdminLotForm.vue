<!-- src/components/AdminLotForm.vue -->
<template>
  <div class="card p-3">
    <h5 class="mb-3">{{ isEdit ? 'Edit Lot' : 'Create Parking Lot' }}</h5>
    <form @submit.prevent="onSubmit">
      <div class="mb-2">
        <label class="form-label">Name</label>
        <input v-model="form.prime_location_name" class="form-control" required />
      </div>
      <div class="mb-2">
        <label class="form-label">Address</label>
        <input v-model="form.address" class="form-control" required />
      </div>

      <div class="row g-2">
        <div class="col">
          <label class="form-label">Pin code</label>
          <input v-model="form.pin_code" class="form-control" required />
        </div>
        <div class="col">
          <label class="form-label">Price / hr</label>
          <input type="number" v-model.number="form.price_per_hour" class="form-control" required />
        </div>
        <div class="col">
          <label class="form-label">Number of spots</label>
          <input type="number" v-model.number="form.number_of_spots" class="form-control" min="0" required />
        </div>
      </div>

      <div class="mt-3 text-end">
        <button class="btn btn-secondary me-2" type="button" @click="$emit('cancel')">Cancel</button>
        <button class="btn btn-primary" type="submit">{{ isEdit ? 'Save' : 'Create' }}</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    initial: { type: Object, default: () => ({}) }
  },
  data() {
    return {
      form: {
        prime_location_name: this.initial.prime_location_name || '',
        address: this.initial.address || '',
        pin_code: this.initial.pin_code || '',
        price_per_hour: this.initial.price_per_hour ?? 0,
        number_of_spots: this.initial.number_of_spots ?? 0,
        id: this.initial.id
      }
    }
  },
  computed: {
    isEdit() { return !!this.form.id }
  },
  methods: {
    onSubmit() { this.$emit('save', { ...this.form }) }
  }
}
</script>
