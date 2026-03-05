<template>
  <div class="room-layout">
    <!-- Gallery -->
    <RoomGallery />

    <!-- Booking panel -->
    <div class="booking-panel">
      <p class="avail-note">📅 Available: Apr 25 – Jun 29, 2026</p>
      <RentCalendar v-model:selection="selection" />

      <!-- Price summary -->
      <div v-if="selection.start" class="price-summary">
        <div class="price-big">${{ totalPrice }} USD</div>
        <div class="date-range">
          {{ formatDate(selection.start) }} –
          {{ selection.end ? formatDate(selection.end) : '...' }}
          <span v-if="nights > 0"> &nbsp; total {{ nights }} night{{ nights > 1 ? 's' : '' }}</span>
        </div>
        <button class="btn-primary" :disabled="!selection.end" @click="showConfirm = true">
          Confirm
        </button>
      </div>
      <p v-else class="mt-16 text-sm text-muted">請選擇入住與退房日期</p>
    </div>
  </div>

  <!-- Modals -->
  <RentConfirmModal
    v-model="showConfirm"
    :selection="selection"
    :nights="nights"
    :total-price="totalPrice"
    @confirmed="onConfirmed"
  />
  <RentSuccessModal
    v-model="showSuccess"
    :reservation="lastReservation"
    :nights="nights"
    :total-price="totalPrice"
    :selection="selection"
  />
</template>

<script setup>
import { ref, computed } from 'vue'
import RoomGallery from '@/components/rent/RoomGallery.vue'
import RentCalendar from '@/components/rent/RentCalendar.vue'
import RentConfirmModal from '@/components/rent/RentConfirmModal.vue'
import RentSuccessModal from '@/components/rent/RentSuccessModal.vue'

const RATE_PER_NIGHT = 222
const selection = ref({ start: null, end: null })
const showConfirm = ref(false)
const showSuccess = ref(false)
const lastReservation = ref(null)

const nights = computed(() => {
  if (!selection.value.start || !selection.value.end) return 0
  return Math.round((selection.value.end - selection.value.start) / (1000 * 60 * 60 * 24))
})
const totalPrice = computed(() => nights.value * RATE_PER_NIGHT)

function formatDate(d) {
  if (!d) return ''
  return `${d.getMonth() + 1}/${d.getDate()}/${String(d.getFullYear()).slice(2)}`
}

function onConfirmed(formData) {
  lastReservation.value = formData
  showConfirm.value = false
  showSuccess.value = true
}
</script>

<style scoped>
.room-layout { display: flex; gap: 28px; flex-wrap: wrap; }
.booking-panel { flex: 1; min-width: 280px; }
.avail-note { font-size: 0.82rem; color: var(--mid); margin-bottom: 12px; }
.price-summary { margin-top: 16px; padding-top: 14px; border-top: 1.5px solid var(--border); }
.price-big { font-size: 1.4rem; font-weight: 700; color: var(--charcoal); }
.date-range { font-size: 0.8rem; color: var(--mid); margin: 4px 0 12px; }
</style>
