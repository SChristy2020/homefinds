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

  async function updateDepositPaid(reservationId) {
    const result = await api.put(`/api/reservations/${reservationId}/deposit-paid`)
    const idx = reservations.value.findIndex(r => r.id === reservationId)
    if (idx !== -1) reservations.value[idx] = result
    sessionStorage.setItem(RESERVATIONS_KEY, JSON.stringify(reservations.value))
    return result
  }

  async function updateDepositUnpaid(reservationId) {
    const result = await api.put(`/api/reservations/${reservationId}/deposit-unpaid`)
    const idx = reservations.value.findIndex(r => r.id === reservationId)
    if (idx !== -1) reservations.value[idx] = result
    sessionStorage.setItem(RESERVATIONS_KEY, JSON.stringify(reservations.value))
    return result
  }

  async function updateFullyPaid(reservationId) {
    const result = await api.put(`/api/reservations/${reservationId}/fully-paid`)
    const idx = reservations.value.findIndex(r => r.id === reservationId)
    if (idx !== -1) reservations.value[idx] = result
    sessionStorage.setItem(RESERVATIONS_KEY, JSON.stringify(reservations.value))
    return result
  }

  async function updateFullyUnpaid(reservationId) {
    const result = await api.put(`/api/reservations/${reservationId}/fully-unpaid`)
    const idx = reservations.value.findIndex(r => r.id === reservationId)
    if (idx !== -1) reservations.value[idx] = result
    sessionStorage.setItem(RESERVATIONS_KEY, JSON.stringify(reservations.value))
    return result
  }

  function clearReservations() {
    reservations.value = []
    sessionStorage.removeItem(RESERVATIONS_KEY)
  }

  return { reservations, fetchReservationsByUser, fetchAllReservations, updateDepositPaid, updateDepositUnpaid, updateFullyPaid, updateFullyUnpaid, clearReservations }
})
