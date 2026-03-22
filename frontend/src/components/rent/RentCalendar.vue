<template>
  <div class="calendar">
    <div class="cal-header">
      <button class="cal-nav" @click="prevMonth"><ChevronLeft :size="16" /></button>
      <span class="cal-month">{{ title }}</span>
      <button class="cal-nav" @click="nextMonth"><ChevronRight :size="16" /></button>
    </div>
    <div class="cal-grid">
      <div class="cal-weekday" v-for="d in weekdays" :key="d">{{ d }}</div>
      <div
        v-for="(day, i) in days"
        :key="i"
        class="cal-day"
        :class="getDayClass(day)"
        @click="selectDay(day)"
      >
        {{ day ? day.date : '' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({
  selection: Object,
  rentStart: Date,
  rentEnd: Date,
  blockedRanges: { type: Array, default: () => [] }, // [{ check_in: 'YYYY-MM-DD', check_out: 'YYYY-MM-DD' }]
})
const emit = defineEmits(['update:selection'])

const i18n = useI18nStore()

const weekdays = computed(() => i18n.t('calendar.weekdays'))
const months   = computed(() => i18n.t('calendar.months'))

const year  = ref(props.rentStart ? props.rentStart.getFullYear() : new Date().getFullYear())
const month = ref(props.rentStart ? props.rentStart.getMonth() : new Date().getMonth())

watch(() => props.rentStart, (val) => {
  if (val) { year.value = val.getFullYear(); month.value = val.getMonth() }
}, { immediate: false })

const title = computed(() => {
  return i18n.t('calendar.titleFormat', { year: year.value, month: months.value[month.value] })
})

function prevMonth() {
  if (month.value === 0) { month.value = 11; year.value-- }
  else month.value--
}
function nextMonth() {
  if (month.value === 11) { month.value = 0; year.value++ }
  else month.value++
}

const days = computed(() => {
  const first = new Date(year.value, month.value, 1)
  const last  = new Date(year.value, month.value + 1, 0)
  const dow = first.getDay() // 0=Sun, already correct for Sunday-first layout
  const list = Array(dow).fill(null)
  for (let d = 1; d <= last.getDate(); d++) {
    list.push({ date: d, full: new Date(year.value, month.value, d) })
  }
  return list
})

// 解析 blocked ranges 為 Date 物件（只解析一次，避免重複）
const parsedBlockedRanges = computed(() =>
  props.blockedRanges.map(r => ({
    checkIn:  new Date(r.check_in  + 'T00:00:00'),
    checkOut: new Date(r.check_out + 'T00:00:00'),
  }))
)

// 判斷某日是否在已封鎖範圍內（check_in <= d < check_out）
function isBlocked(d) {
  return parsedBlockedRanges.value.some(r => d >= r.checkIn && d < r.checkOut)
}

// 選退房日時的封鎖判斷：r.checkIn 當天可作為退房日（我退＝對方入住，不衝突）
function isBlockedForCheckOut(d) {
  return parsedBlockedRanges.value.some(r => d > r.checkIn && d < r.checkOut)
}

// 判斷 [start, end] 範圍是否與任何 blocked range 重疊
function rangeOverlapsBlocked(start, end) {
  return parsedBlockedRanges.value.some(r => start < r.checkOut && end > r.checkIn)
}

function getDayClass(day) {
  if (!day) return 'empty'
  const d = day.full
  if (!props.rentStart || !props.rentEnd || d < props.rentStart || d > props.rentEnd) return 'disabled'
  const selectingEnd = !!(props.selection.start && !props.selection.end)
  if (selectingEnd ? isBlockedForCheckOut(d) : isBlocked(d)) return 'blocked'
  const { start, end } = props.selection
  const today = new Date(); today.setHours(0,0,0,0)
  if (start && d.toDateString() === start.toDateString()) return 'selected-start'
  if (end   && d.toDateString() === end.toDateString())   return 'selected-end'
  if (start && end && d > start && d < end) return 'in-range'
  if (d.toDateString() === today.toDateString()) return 'today'
  return ''
}

function selectDay(day) {
  if (!day) return
  const d = day.full
  if (!props.rentStart || !props.rentEnd || d < props.rentStart || d > props.rentEnd) return
  const { start, end } = props.selection
  const selectingEnd = !!(start && !end)
  if (selectingEnd ? isBlockedForCheckOut(d) : isBlocked(d)) return
  if (!start || (start && end) || d < start) {
    emit('update:selection', { start: d, end: null })
  } else if (d.toDateString() !== start.toDateString()) {
    // 若選取的範圍與已封鎖時段重疊，不允許選取
    if (rangeOverlapsBlocked(start, d)) return
    emit('update:selection', { start, end: d })
  }
}
</script>

<style scoped>
.calendar { font-size: 0.82rem; }
.cal-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.cal-nav {
  background: none; border: none; cursor: pointer;
  color: var(--mid); padding: 2px 4px;
  border-radius: 2px; transition: color 0.15s;
  display: flex; align-items: center;
}
.cal-nav:hover { color: var(--charcoal); }
.cal-month { font-weight: 600; font-size: 0.88rem; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; }
.cal-weekday { text-align: center; color: var(--mid); padding: 4px 0; font-size: 0.72rem; }
.cal-day {
  text-align: center; padding: 6px 2px;
  border-radius: 3px; cursor: pointer;
  transition: all 0.15s; font-size: 0.8rem;
  border: 1.5px solid transparent;
}
.cal-day:hover:not(.disabled):not(.empty):not(.blocked) { background: var(--button); }
.cal-day.empty    { cursor: default; }
.cal-day.disabled { color: var(--button); cursor: not-allowed; text-decoration: line-through; }
.cal-day.blocked  { color: var(--button); cursor: not-allowed; background: var(--accent-light); text-decoration: line-through; }
.cal-day.in-range { background: var(--light); }
.cal-day.selected-start,
.cal-day.selected-end    { background: var(--accent); color: #fff; }
.cal-day.today    { border-color: var(--accent); font-weight: 600; }
</style>
