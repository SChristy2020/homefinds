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
          <select class="pdp-select" :value="hourValue" @change="hourValue = $event.target.value">
            <option v-for="h in hours" :key="h" :value="h">{{ h }}</option>
          </select>
          <span class="pdp-colon">:</span>
          <select class="pdp-select" :value="minuteValue" @change="minuteValue = $event.target.value">
            <option v-for="m in minutes" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>

      <!-- Confirm -->
      <div class="pdp-footer">
        <button class="pdp-confirm" @click.stop="confirm">{{ confirmLabel }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ChevronDown, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({ modelValue: String, placeholder: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue'])

const i18n = useI18nStore()
const root = ref(null)
const open = ref(false)

const today = new Date(); today.setHours(0,0,0,0)

const DEFAULT_DATE = new Date(2026, 3, 18) // April 18, 2026
const DEFAULT_HOUR = '14'
const DEFAULT_MIN  = '00'
const CUTOFF_DATE  = new Date(2026, 3, 25) // April 25, 2026 — no dates after this

const viewYear  = ref(DEFAULT_DATE.getFullYear())
const viewMonth = ref(DEFAULT_DATE.getMonth())

const selectedDate = ref(DEFAULT_DATE)
const hourValue    = ref(DEFAULT_HOUR)
const minuteValue  = ref(DEFAULT_MIN)

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

// Hour & minute options
const hours   = Array.from({ length: 12 }, (_, i) => String(i + 10).padStart(2, '0')) // 10:00–21:00
const minutes = ['00', '15', '30', '45']

const isEn = computed(() => i18n.locale === 'en')

// Weekday headers — Sun-first for English, Mon-first for Chinese
const EN_WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const weekdayHeaders = computed(() =>
  isEn.value ? EN_WEEKDAYS : i18n.t('calendar.weekdays')
)

const months = computed(() => i18n.t('calendar.months'))

const monthLabel = computed(() => {
  const fmt = i18n.t('calendar.titleFormat')
  return fmt.replace('{year}', viewYear.value).replace('{month}', months.value[viewMonth.value])
})
const timeLabel    = computed(() => isEn.value ? 'Time' : '時間')
const confirmLabel = computed(() => isEn.value ? 'OK' : '確認')

const displayValue = computed(() => {
  if (!selectedDate.value) return ''
  const d = selectedDate.value
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()} ${hourValue.value}:${minuteValue.value}`
})

// Offset: Sun-first (en) vs Mon-first (zh)
function startOffset(firstDayOfMonth) {
  const dow = firstDayOfMonth.getDay() // 0=Sun
  return isEn.value ? dow : (dow === 0 ? 6 : dow - 1)
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
  if (d < today || d > CUTOFF_DATE) return 'disabled'
  if (selectedDate.value && d.toDateString() === selectedDate.value.toDateString()) return 'selected'
  if (d.toDateString() === today.toDateString()) return 'today'
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
  if (!day || day.full < today || day.full > CUTOFF_DATE) return
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
.pdp-confirm:hover { opacity: 0.85; }
</style>
