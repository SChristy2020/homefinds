import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'

export const PICKUP_DEFAULTS = {
  endDate: '2026-04-25',
  defaultDate: '2026-04-18',
  startHour: 10,
  endHour: 20,
  defaultHour: 15,
  defaultMinute: '00',
  minuteInterval: 15,
  minutes: ['00', '15', '30', '45'],
  // [{ date: 'YYYY-MM-DD', startHour: 14, endHour: 16 }]
  blockedRanges: [],
}

export const usePickupSettingsStore = defineStore('pickupSettings', () => {
  const settings = ref({ ...PICKUP_DEFAULTS })

  async function fetch() {
    try {
      const data = await api.get('/api/pickup-settings')
      settings.value = { ...PICKUP_DEFAULTS, ...data }
    } catch {
      // 若 API 失敗，沿用預設值
    }
  }

  async function save(newSettings) {
    settings.value = { ...settings.value, ...newSettings }
    await api.put('/api/pickup-settings', settings.value)
  }

  return { settings, fetch, save }
})
