<template>
  <div class="rent-page">
  <h1 class="rent-title">{{ i18n.t('rent.title') }}</h1>
  <div class="room-layout">
    <!-- Gallery -->
    <RoomGallery :images="roomImages" />

    <!-- Booking panel -->
    <div class="booking-panel">
      <p class="avail-note"><CalendarDays :size="14" /> {{ availNote }}</p>
      <RentCalendar v-model:selection="selection" :rent-start="rentStart" :rent-end="rentEnd" />

      <!-- Price summary -->
      <div v-if="selection.start" class="price-summary">
        <div class="price-row">
          <span v-if="nights >= 7 && originalPrice > totalPrice" class="price-original">${{ originalPrice }} USD</span>
          <span class="price-big">${{ totalPrice }} USD</span>
        </div>
        <div class="date-range">
          {{ formatDate(selection.start) }} –
          {{ selection.end ? formatDate(selection.end) : '...' }}
          <span v-if="nights > 0"> &nbsp; {{ i18n.t('rent.total') }} {{ nights }} {{ nights === 1 ? i18n.t('rent.night') : i18n.t('rent.nights') }}</span>
        </div>
        <button class="btn-primary" :disabled="!selection.end" @click="showConfirm = true">
          {{ i18n.t('rent.confirm') }}
        </button>
      </div>
      <p v-else class="mt-16 text-sm text-muted">{{ i18n.t('rent.selectDates') }}</p>
    </div>
  </div>
  </div>

  <!-- Description -->
  <div v-if="roomDescription" class="room-description" v-html="roomDescription"></div>

  <!-- Modals -->
  <RentConfirmModal
    v-model="showConfirm"
    :selection="selection"
    :nights="nights"
    :total-price="totalPrice"
    :booking-description="roomBookingDescription"
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
import { ref, computed, onMounted } from 'vue'
import { CalendarDays } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'
import { api } from '@/utils/api'
import RoomGallery from '@/components/rent/RoomGallery.vue'
import RentCalendar from '@/components/rent/RentCalendar.vue'
import RentConfirmModal from '@/components/rent/RentConfirmModal.vue'
import RentSuccessModal from '@/components/rent/RentSuccessModal.vue'

const i18n = useI18nStore()
const room = ref(null)
const selection = ref({ start: null, end: null })
const roomTranslations = ref({})
const roomImages = ref([])

const rentStart = computed(() => room.value?.available_from ? new Date(room.value.available_from + 'T00:00:00') : null)
const rentEnd   = computed(() => room.value?.available_to   ? new Date(room.value.available_to   + 'T00:00:00') : null)

const availNote = computed(() => {
  const base = i18n.t('rent.available')
  if (!rentStart.value || !rentEnd.value) return base
  const fmt = d => `${d.getMonth() + 1}/${d.getDate()}/${d.getFullYear()}`
  return `${base} ${fmt(rentStart.value)} – ${fmt(rentEnd.value)}`
})

const roomDescription = computed(() => roomTranslations.value[i18n.locale]?.description || '')
const roomBookingDescription = computed(() => roomTranslations.value[i18n.locale]?.booking_description || '')
const showConfirm = ref(false)
const showSuccess = ref(false)
const lastReservation = ref(null)

const nights = computed(() => {
  if (!selection.value.start || !selection.value.end) return 0
  return Math.round((selection.value.end - selection.value.start) / (1000 * 60 * 60 * 24))
})

const originalPrice = computed(() => {
  const n = nights.value
  if (!n || !room.value) return 0
  return Math.round(n * Number(room.value.price_per_night || 0))
})

const totalPrice = computed(() => {
  const n = nights.value
  if (!n || !room.value) return 0
  const { price_per_night, price_7_nights, price_30_days, price_full_period } = room.value

  // 全租期間
  if (price_full_period && rentStart.value && rentEnd.value) {
    const fullNights = Math.round((rentEnd.value - rentStart.value) / (1000 * 60 * 60 * 24))
    if (n === fullNights) return Number(price_full_period)
  }

  let remaining = n
  let total = 0
  if (price_30_days && remaining >= 30) {
    const months = Math.floor(remaining / 30)
    total += months * Number(price_30_days)
    remaining -= months * 30
  }
  if (price_7_nights && remaining >= 7) {
    const weeks = Math.floor(remaining / 7)
    total += weeks * Number(price_7_nights)
    remaining -= weeks * 7
  }
  total += remaining * Number(price_per_night || 0)
  return Math.round(total)
})

function formatDate(d) {
  if (!d) return ''
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
}

function onConfirmed(formData) {
  lastReservation.value = formData
  showConfirm.value = false
  showSuccess.value = true
}

onMounted(async () => {
  try {
    const rooms = await api.get('/api/room')
    if (rooms.length) {
      const r = rooms[0]
      room.value = r
      roomImages.value = (r.images || []).sort((a, b) => a.sort_order - b.sort_order)
      const map = {}
      for (const t of (r.translations || [])) {
        map[t.locale] = { description: t.description || '', booking_description: t.booking_description || '' }
      }
      roomTranslations.value = map
      // 預設選取全部租期
      if (rentStart.value && rentEnd.value) {
        selection.value = { start: rentStart.value, end: rentEnd.value }
      }
    }
  } catch {}
})
</script>

<style scoped>
.rent-page { display: flex; flex-direction: column; gap: 16px; }
.rent-title { font-size: 1.3rem; font-weight: 700; text-align: center; color: var(--charcoal); margin: 0 0 4px; }
.room-layout { display: flex; gap: 28px; flex-wrap: wrap; }
.booking-panel { flex: 1; min-width: 280px; }
.avail-note { font-size: 1rem; color: var(--mid); margin-bottom: 12px; display: flex; align-items: center; gap: 5px; }
.price-summary { margin-top: 16px; padding-top: 14px; border-top: 1.5px solid var(--border); }
.price-row { display: flex; align-items: baseline; gap: 8px; }
.price-original { font-size: 1rem; color: var(--mid); text-decoration: line-through; }
.price-big { font-size: 1.6rem; font-weight: 700; color: var(--charcoal); }
.date-range { font-size: 1rem; color: var(--mid); margin: 4px 0 12px; }
.room-description { font-size: 1rem; color: var(--charcoal); line-height: 1.7; padding: 2rem 1rem; }
.room-description :deep(ul), .room-description :deep(ol) { padding-left: 1.5em; }
.room-description :deep(ul) { list-style-type: disc; }
.room-description :deep(ol) { list-style-type: decimal; }
.room-description :deep(ul ul) { list-style-type: circle; }
.room-description :deep(ul ul ul) { list-style-type: square; }
.room-description :deep(blockquote) { margin-left: 1.5em; padding-left: 0.75em; border-left: 3px solid var(--border); }
</style>
