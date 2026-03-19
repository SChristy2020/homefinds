import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'

const RESERVATIONS_KEY = 'homefinds_reservations'

export const useReservationsStore = defineStore('reservations', () => {
  const reservations = ref(JSON.parse(sessionStorage.getItem(RESERVATIONS_KEY)) || [])

  async function fetchReservationsByUser(userId) {
    const result = await api.get(`/api/reservations/user/${userId}`)
    reservations.value = result
    sessionStorage.setItem(RESERVATIONS_KEY, JSON.stringify(result))
    return result
  }

  async function fetchAllReservations() {
    const result = await api.get('/api/reservations/all')
    reservations.value = result
    sessionStorage.setItem(RESERVATIONS_KEY, JSON.stringify(result))
    return result
  }

  function mergeResult(reservationId, result) {
    const idx = reservations.value.findIndex(r => r.id === reservationId)
    if (idx !== -1) reservations.value[idx] = { ...reservations.value[idx], ...result }
    sessionStorage.setItem(RESERVATIONS_KEY, JSON.stringify(reservations.value))
  }

  async function updateOrderStatus(reservationId, orderStatus) {
    const result = await api.put(`/api/reservations/${reservationId}/status`, { order_status: orderStatus })
    mergeResult(reservationId, result)
    return result
  }

  function clearReservations() {
    reservations.value = []
    sessionStorage.removeItem(RESERVATIONS_KEY)
  }

  return { reservations, fetchReservationsByUser, fetchAllReservations, updateOrderStatus, clearReservations }
})
