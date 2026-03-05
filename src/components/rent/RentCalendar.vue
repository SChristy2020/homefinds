<template>
  <div class="calendar">
    <div class="cal-header">
      <button class="cal-nav" @click="prevMonth">‹</button>
      <span class="cal-month">{{ title }}</span>
      <button class="cal-nav" @click="nextMonth">›</button>
    </div>
    <div class="cal-grid">
      <div class="cal-weekday" v-for="d in WEEKDAYS" :key="d">{{ d }}</div>
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
import { ref, computed } from 'vue'

const props = defineProps({ selection: Object })
const emit = defineEmits(['update:selection'])

const RENT_START = new Date(2026, 3, 25)
const RENT_END   = new Date(2026, 5, 29)
const WEEKDAYS   = ['一','二','三','四','五','六','日']
const MONTHS     = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']

const year  = ref(2026)
const month = ref(3) // April (0-indexed)

const title = computed(() => `${year.value}年 ${MONTHS[month.value]}`)

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
  let dow = first.getDay()
  dow = dow === 0 ? 6 : dow - 1
  const list = Array(dow).fill(null)
  for (let d = 1; d <= last.getDate(); d++) {
    list.push({ date: d, full: new Date(year.value, month.value, d) })
  }
  return list
})

function getDayClass(day) {
  if (!day) return 'empty'
  const d = day.full
  if (d < RENT_START || d > RENT_END) return 'disabled'
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
  if (d < RENT_START || d > RENT_END) return
  const { start, end } = props.selection
  if (!start || (start && end) || d < start) {
    emit('update:selection', { start: d, end: null })
  } else if (d.toDateString() !== start.toDateString()) {
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
  font-size: 1rem; color: var(--mid); padding: 2px 6px;
  border-radius: 2px; transition: color 0.15s;
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
.cal-day:hover:not(.disabled):not(.empty) { background: var(--accent-light); }
.cal-day.empty    { cursor: default; }
.cal-day.disabled { color: var(--light); cursor: not-allowed; text-decoration: line-through; }
.cal-day.in-range { background: var(--accent-light); }
.cal-day.selected-start,
.cal-day.selected-end    { background: var(--charcoal); color: #fff; }
.cal-day.today    { border-color: var(--accent); font-weight: 600; }
</style>
