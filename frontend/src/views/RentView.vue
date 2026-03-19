<template>
  <div class="rent-page">
  <h1 class="rent-title">{{ i18n.t('rent.title') }}</h1>
  <div class="room-layout">
    <!-- Gallery -->
    <RoomGallery :images="roomImages" />

    <!-- Booking panel -->
    <div class="booking-panel">
      <p class="avail-note"><CalendarDays :size="14" /> {{ availNote }}</p>

      <RentCalendar v-model:selection="selection" :rent-start="rentStart" :rent-end="rentEnd" :blocked-ranges="blockedRanges" />

      <!-- Price summary -->
      <div v-if="selection.start" class="price-summary">
        <!-- Date row -->
        <div class="date-row">
          <div class="date-col">
            <span class="date-col-label">{{ i18n.t('rent.checkIn') }}</span>
            <span class="date-col-value">{{ formatDate(selection.start) }}</span>
          </div>
          <span class="date-arrow">→</span>
          <div class="date-col">
            <span class="date-col-label">{{ i18n.t('rent.checkOut') }}</span>
            <span class="date-col-value">{{ selection.end ? formatDate(selection.end) : '...' }}</span>
          </div>
          <span v-if="nights > 0" class="nights-badge">{{ i18n.t('rent.totalStay') }}{{ nights }}{{ i18n.t('rent.totalStaySuffix') }}</span>
        </div>

        <!-- Original price row -->
        <div class="price-line">
          <span class="price-line-label">{{ i18n.t('rent.originalLabel') }}</span>
          <span class="price-line-value price-original">USD {{ originalPrice }}</span>
        </div>

        <!-- Special price row -->
        <div class="price-line">
          <span class="price-line-label">{{ i18n.t('rent.specialLabel') }}</span>
          <span class="price-line-value price-special" :class="{ strikethrough: isEarlyBird }">USD {{ totalPrice }}</span>
        </div>

        <!-- Early bird (if booking in March) -->
        <div v-if="isEarlyBird" class="price-line early-bird-line">
          <span class="price-line-label early-bird-label">{{ i18n.t('rent.earlyBirdLabel') }}</span>
          <span class="price-line-value early-bird-price">USD {{ earlyBirdPrice }}</span>
          <span class="early-bird-note">{{ i18n.t('rent.earlyBirdNote') }}</span>
        </div>

        <button class="btn-primary book-btn" :disabled="!selection.end" @click="showConfirm = true">
          {{ i18n.t('rent.bookNow') }}
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
    :total-price="finalPrice"
    :original-price="originalPrice"
    :special-price="totalPrice"
    :early-bird-price="earlyBirdPrice"
    :is-early-bird="isEarlyBird"
    :booking-description="roomBookingDescription"
    @confirmed="onConfirmed"
  />
  <RentSuccessModal
    v-model="showSuccess"
    :reservation="lastReservation"
    :nights="nights"
    :total-price="finalPrice"
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
const blockedRanges = ref([])

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

// 早鳥：3月預訂再9折
const isEarlyBird = computed(() => new Date().getMonth() === 2) // March = index 2
const earlyBirdPrice = computed(() => Math.round(totalPrice.value * 0.9))
const finalPrice = computed(() => isEarlyBird.value ? earlyBirdPrice.value : totalPrice.value)

function formatDate(d) {
  if (!d) return ''
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
}

function onConfirmed(formData) {
  lastReservation.value = formData
}

onMounted(async () => {
  try {
    const [rooms, blocked] = await Promise.all([
      api.get('/api/room'),
      api.get('/api/reservations/blocked-dates').catch(() => []),
    ])
    blockedRanges.value = blocked || []
    if (rooms.length) {
      const r = rooms[0]
      room.value = r
      roomImages.value = (r.images || []).sort((a, b) => a.sort_order - b.sort_order)
      const map = {}
      for (const t of (r.translations || [])) {
        map[t.locale] = { description: t.description || '', booking_description: t.booking_description || '' }
      }
      roomTranslations.value = map
      // 預設選取日期區間
      if (rentStart.value && rentEnd.value) {
        const parsed = (blocked || []).map(r => ({
          checkIn:  new Date(r.check_in  + 'T00:00:00'),
          checkOut: new Date(r.check_out + 'T00:00:00'),
        }))
        const isBlockedDay = (d) => parsed.some(r => d >= r.checkIn && d < r.checkOut)
        // 找第一個未封鎖的入住日
        let defaultStart = new Date(rentStart.value)
        while (defaultStart < rentEnd.value && isBlockedDay(defaultStart)) {
          defaultStart.setDate(defaultStart.getDate() + 1)
        }
        // 退房日為 defaultStart 之後最近的已訂訂單入住日（若無則為 rentEnd）
        const nextCheckIn = parsed
          .map(r => r.checkIn)
          .filter(d => d > defaultStart)
          .sort((a, b) => a - b)[0]
        const defaultEnd = nextCheckIn && nextCheckIn <= rentEnd.value ? nextCheckIn : rentEnd.value
        selection.value = { start: defaultStart, end: defaultEnd }
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

/* Avail note */
.avail-note { font-size: 1rem; color: var(--mid); margin-bottom: 12px; display: flex; align-items: center; gap: 5px; }

/* Price summary card */
.price-summary { margin-top: 16px; padding: 16px 20px; border-radius: 10px; display: flex; flex-direction: column; gap: 2px; background: rgb(255 255 255 / 60%); box-shadow: 3px 3px 11px 1px #cccc; transition: .2s;}
.price-summary:hover { background: rgb(255 255 255 / 80%); box-shadow: 3px 3px 11px 1px #7d7d7dcc;}

/* Date row */
.date-row { display: flex; align-items: center; gap: 8px; padding-bottom: 4px; margin-bottom: 6px;border-bottom: 1px solid var(--border); }
.date-col { display: flex; flex-direction: column; gap: 2px; }
.date-col-label { font-size: 0.78rem; color: var(--mid); }
.date-col-value { font-size: 0.95rem; font-weight: 600; color: var(--charcoal); }
.date-arrow { font-size: 1.1rem; color: var(--mid); padding: 0 4px; margin-top: 10px; }
.nights-badge { margin-left: auto; font-size: 0.95rem; font-weight: 600; color: var(--charcoal); white-space: nowrap; }

/* Price lines */
.price-line { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
.price-line-label { font-size: 0.95rem; color: var(--charcoal); min-width: 5em; }
.price-line-value { font-size: 1rem; }
.price-original { color: var(--mid); text-decoration: line-through; }
.price-special { font-size: 1.5rem; font-weight: 700; color: var(--charcoal);}

/* Early bird */
.early-bird-line { color: #c0392b; }
.early-bird-label { font-weight: 600; color: #c0392b; }
.early-bird-price { font-size: 1.5rem; font-weight: 800; color: #c0392b; }
.early-bird-note { font-weight: 500; color: #c0392b; margin-top: -14px;}

.book-btn { width: 100%; }

.room-description { font-size: 1rem; color: var(--charcoal); line-height: 1.7; padding: 2rem 1rem; }
.room-description :deep(ul), .room-description :deep(ol) { padding-left: 1.5em; }
.room-description :deep(ul) { list-style-type: disc; }
.room-description :deep(ol) { list-style-type: decimal; }
.room-description :deep(ul ul) { list-style-type: circle; }
.room-description :deep(ul ul ul) { list-style-type: square; }
.room-description :deep(blockquote) { margin-left: 1.5em; padding-left: 0.75em; border-left: 3px solid var(--border); }
.room-description :deep(iframe) { width: 100% !important; max-width: 100%; height: 400px; border: none; border-radius: 6px; display: block; margin: 8px 0; }
.room-description :deep(.map-embed) { width: 100%; }
</style>
