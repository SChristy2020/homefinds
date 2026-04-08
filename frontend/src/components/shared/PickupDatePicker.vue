<template>
  <div class="pdp" ref="root">
    <!-- Trigger input -->
    <div class="pdp-input" :class="{ open }" @click="open = !open">
      <span :class="{ placeholder: !displayValue }">{{ displayValue || placeholder }}</span>
      <ChevronDown :size="14" class="pdp-chevron" :class="{ rotated: open }" />
    </div>

    <!-- Popover -->
    <div v-if="open" class="pdp-popover">
      <!-- Calendar -->
      <div class="pdp-cal-header">
        <button class="pdp-nav" @click.stop="prevMonth"><ChevronLeft :size="14" /></button>
        <span class="pdp-month-label">{{ monthLabel }}</span>
        <button class="pdp-nav" @click.stop="nextMonth"><ChevronRight :size="14" /></button>
      </div>
      <div class="pdp-grid">
        <div class="pdp-weekday" v-for="d in weekdayHeaders" :key="d">{{ d }}</div>
        <div
          v-for="(day, i) in days"
          :key="i"
          class="pdp-day"
          :class="getDayClass(day)"
          @click.stop="selectDate(day)"
        >{{ day ? day.date : '' }}</div>
      </div>

      <!-- Time -->
      <div class="pdp-time-row">
        <span class="pdp-time-label">{{ timeLabel }}</span>
        <div class="pdp-time-selects" @click.stop>
          <select class="pdp-select" :value="hourValue" @change="onHourChange($event.target.value)">
            <option v-for="h in hours" :key="h" :value="h" :disabled="isHourFull(h)">
              {{ h }}{{ isHourFull(h) ? (isEn ? ' (Full)' : i18n.locale === 'zh-CN' ? ' (此时段已满)' : ' (此時段已滿)') : '' }}
            </option>
          </select>
          <span class="pdp-colon">:</span>
          <select class="pdp-select" :value="minuteValue" @change="minuteValue = $event.target.value">
            <option v-for="m in minutes" :key="m" :value="m" :disabled="isSlotBooked(hourValue, m)">
              {{ m }}{{ isSlotBooked(hourValue, m) ? (isEn ? ' (Already booked)' : i18n.locale === 'zh-CN' ? ' (已被预约)' : ' (已被預約)') : '' }}
            </option>
          </select>
        </div>
      </div>
      <div v-if="currentSlotBooked" class="pdp-slot-error">{{ slotBookedLabel }}</div>

      <!-- Confirm -->
      <div class="pdp-footer">
        <button class="pdp-confirm" :disabled="currentSlotBooked" @click.stop="confirm">{{ confirmLabel }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { ChevronDown, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'
import { usePickupSettingsStore } from '@/stores/pickupSettings'

const props = defineProps({
  modelValue: String,
  placeholder: { type: String, default: '' },
  bookedSlots: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:modelValue'])

const i18n = useI18nStore()
const pickupSettings = usePickupSettingsStore()
const root = ref(null)
const open = ref(false)

// 最早可選日期 = 美東今天 + 1 天
const minDate = computed(() => {
  const etNow = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/New_York' }))
  etNow.setHours(0, 0, 0, 0)
  etNow.setDate(etNow.getDate() + 1)
  return etNow
})
const cutoffDate = computed(() => {
  const [y, m, d] = pickupSettings.settings.endDate.split('-').map(Number)
  return new Date(y, m - 1, d)
})

const defaultDate = computed(() => {
  const [y, m, d] = pickupSettings.settings.defaultDate.split('-').map(Number)
  const date = new Date(y, m - 1, d)
  // 若設定的預設日期早於最早可選日期，改用最早可選日期
  return date >= minDate.value ? date : minDate.value
})

const viewYear  = ref(defaultDate.value.getFullYear())
const viewMonth = ref(defaultDate.value.getMonth())

const selectedDate = ref(defaultDate.value)
const hourValue    = ref(String(pickupSettings.settings.defaultHour).padStart(2, '0'))
const minuteValue  = ref(pickupSettings.settings.defaultMinute ?? '00')

// Parse existing modelValue if provided
if (props.modelValue) {
  const parts = props.modelValue.match(/(\d+)\/(\d+)\/(\d+)\s+(\d+):(\d+)/)
  if (parts) {
    selectedDate.value = new Date(+parts[3], +parts[1] - 1, +parts[2])
    hourValue.value    = String(+parts[4]).padStart(2, '0')
    minuteValue.value  = String(+parts[5]).padStart(2, '0')
    viewYear.value     = selectedDate.value.getFullYear()
    viewMonth.value    = selectedDate.value.getMonth()
  }
}

const hours = computed(() => {
  const start = pickupSettings.settings.startHour
  const end   = pickupSettings.settings.endHour
  return Array.from({ length: end - start + 1 }, (_, i) => String(i + start).padStart(2, '0'))
})
const minutes = computed(() => pickupSettings.settings.minutes)

const isEn = computed(() => i18n.locale === 'en')

const weekdayHeaders = computed(() => i18n.t('calendar.weekdays'))

const months = computed(() => i18n.t('calendar.months'))

const monthLabel = computed(() => {
  return i18n.t('calendar.titleFormat', { year: viewYear.value, month: months.value[viewMonth.value] })
})
const timeLabel    = computed(() => isEn.value ? 'Time' : '時間')
const confirmLabel = computed(() => isEn.value ? 'OK' : '確認')
const slotBookedLabel = computed(() => isEn.value ? 'This time slot is taken' : i18n.locale === 'zh-CN' ? '此时段已被预订' : '此時段已被預訂')

function isHourBlocked(hour) {
  if (!selectedDate.value) return false
  const d = selectedDate.value
  const dateStr = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
  const h = typeof hour === 'string' ? parseInt(hour) : hour
  return (pickupSettings.settings.blockedRanges || []).some(r =>
    r.date === dateStr && h >= r.startHour && h < r.endHour
  )
}

function isHourFull(hour) {
  return isHourBlocked(hour) || minutes.value.every(m => isSlotBooked(hour, m))
}

function isSlotBooked(hour, minute) {
  if (!props.bookedSlots?.length || !selectedDate.value) return false
  const d = selectedDate.value
  const dateStr = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
  return props.bookedSlots.includes(`${dateStr}T${hour}:${minute}`)
}

const currentSlotBooked = computed(() => isSlotBooked(hourValue.value, minuteValue.value))

function findNextAvailableSlot() {
  const hourList = hours.value
  const startIdx = hourList.indexOf(hourValue.value)
  for (let i = startIdx; i < hourList.length; i++) {
    for (const m of minutes.value) {
      if (!isSlotBooked(hourList[i], m)) {
        return { hour: hourList[i], minute: m }
      }
    }
  }
  return null
}

watch([() => props.bookedSlots, selectedDate, hourValue], () => {
  if (!currentSlotBooked.value) return
  const next = findNextAvailableSlot()
  if (next) {
    hourValue.value = next.hour
    minuteValue.value = next.minute
    emit('update:modelValue', displayValue.value)
  }
})

function onHourChange(h) {
  hourValue.value = h
  if (isSlotBooked(h, minuteValue.value)) {
    const available = minutes.value.find(m => !isSlotBooked(h, m))
    if (available) minuteValue.value = available
  }
}

const displayValue = computed(() => {
  if (!selectedDate.value) return ''
  const d = selectedDate.value
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()} ${hourValue.value}:${minuteValue.value}`
})

function startOffset(firstDayOfMonth) {
  return firstDayOfMonth.getDay() // 0=Sun, always Sun-first
}

const days = computed(() => {
  const first = new Date(viewYear.value, viewMonth.value, 1)
  const last  = new Date(viewYear.value, viewMonth.value + 1, 0)
  const list  = Array(startOffset(first)).fill(null)
  for (let d = 1; d <= last.getDate(); d++) {
    list.push({ date: d, full: new Date(viewYear.value, viewMonth.value, d) })
  }
  return list
})

function getDayClass(day) {
  if (!day) return 'empty'
  const d = day.full
  if (d < minDate.value || d > cutoffDate.value) return 'disabled'
  if (selectedDate.value && d.toDateString() === selectedDate.value.toDateString()) return 'selected'
  if (d.toDateString() === minDate.value.toDateString()) return 'today'
  return ''
}

function prevMonth() {
  if (viewMonth.value === 0) { viewMonth.value = 11; viewYear.value-- }
  else viewMonth.value--
}
function nextMonth() {
  if (viewMonth.value === 11) { viewMonth.value = 0; viewYear.value++ }
  else viewMonth.value++
}

function selectDate(day) {
  if (!day || day.full < minDate.value || day.full > cutoffDate.value) return
  selectedDate.value = day.full
  emit('update:modelValue', displayValue.value)
}

function confirm() {
  emit('update:modelValue', displayValue.value)
  open.value = false
}

// Emit default on mount if no value
onMounted(() => {
  if (!props.modelValue) emit('update:modelValue', displayValue.value)
})

// Close on outside click
function onOutsideClick(e) {
  if (root.value && !root.value.contains(e.target)) {
    if (open.value) emit('update:modelValue', displayValue.value)
    open.value = false
  }
}
onMounted(() => document.addEventListener('mousedown', onOutsideClick))
onUnmounted(() => document.removeEventListener('mousedown', onOutsideClick))
</script>

<style scoped>
.pdp { position: relative; }

.pdp-input {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius, 6px);
  background: #fff;
  cursor: pointer;
  font-size: 0.88rem;
  transition: border-color 0.15s;
  min-height: 38px;
}
.pdp-input.open,
.pdp-input:hover { border-color: var(--charcoal); }
.pdp-input .placeholder { color: #aaa; }
.pdp-chevron { color: #999; flex-shrink: 0; transition: transform 0.2s; }
.pdp-chevron.rotated { transform: rotate(180deg); }

.pdp-popover {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  z-index: 500;
  background: #fff;
  border: 1.5px solid var(--border);
  border-radius: var(--radius, 6px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.13);
  padding: 12px;
  min-width: 240px;
}

/* Calendar header */
.pdp-cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.pdp-nav {
  background: none; border: none; cursor: pointer;
  color: var(--mid); display: flex; align-items: center;
  padding: 2px 4px; border-radius: 3px;
  transition: color 0.15s;
}
.pdp-nav:hover { color: var(--charcoal); }
.pdp-month-label { font-weight: 600; font-size: 0.85rem; }

/* Day grid */
.pdp-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}
.pdp-weekday {
  text-align: center;
  font-size: 0.68rem;
  color: var(--mid);
  padding: 2px 0 4px;
}
.pdp-day {
  text-align: center;
  padding: 5px 2px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.78rem;
  transition: background 0.12s;
}
.pdp-day:hover:not(.disabled):not(.empty) { background: var(--accent-light, #f5f0e8); }
.pdp-day.empty    { cursor: default; }
.pdp-day.disabled { color: #ccc; cursor: not-allowed; }
.pdp-day.today    { font-weight: 700; color: var(--accent, #c9a96e); }
.pdp-day.selected { background: var(--charcoal, #2a2a2a); color: #fff; }

/* Time row */
.pdp-time-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
}
.pdp-time-label { font-size: 0.8rem; color: var(--mid); white-space: nowrap; }
.pdp-time-selects {
  display: flex;
  align-items: center;
  gap: 4px;
}
.pdp-select {
  border: 1.5px solid var(--border);
  border-radius: 4px;
  padding: 3px 6px;
  font-size: 0.85rem;
  background: #fff;
  cursor: pointer;
}
.pdp-select:focus { outline: none; border-color: var(--charcoal); }
.pdp-colon { font-weight: 600; color: var(--charcoal); }

/* Footer */
.pdp-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
.pdp-confirm {
  background: var(--charcoal, #2a2a2a);
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 5px 16px;
  font-size: 0.82rem;
  cursor: pointer;
  transition: opacity 0.15s;
}
.pdp-confirm:hover:not(:disabled) { opacity: 0.85; }
.pdp-confirm:disabled { opacity: 0.4; cursor: not-allowed; }

.pdp-slot-error {
  font-size: 0.75rem;
  color: #e74c3c;
  margin-top: 6px;
  text-align: center;
}
</style>
