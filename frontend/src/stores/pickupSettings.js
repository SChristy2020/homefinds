import { defineStore } from 'pinia'
import { ref } from 'vue'

const STORAGE_KEY = 'pickup_settings'

export const PICKUP_DEFAULTS = {
  endDate: '2026-04-25',
  defaultDate: '2026-04-18',
  startHour: 10,
  endHour: 20,
  defaultHour: 15,
  defaultMinute: '00',
  minutes: ['00', '15', '30', '45'],
}

export const usePickupSettingsStore = defineStore('pickupSettings', () => {
  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) return { ...PICKUP_DEFAULTS, ...JSON.parse(raw) }
    } catch {}
    return { ...PICKUP_DEFAULTS }
  }

  const settings = ref(load())

  function save(newSettings) {
    settings.value = { ...settings.value, ...newSettings }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings.value))
  }

  return { settings, save }
})
