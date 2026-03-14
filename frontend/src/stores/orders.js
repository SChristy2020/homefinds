// stores/orders.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'
import { useI18nStore } from '@/stores/i18n'

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref([])

  async function createOrder(formData, cartItems) {
    // 1. 查找現有 user，若無則建立
    let user
    try {
      const params = new URLSearchParams({
        last_name: formData.lastName,
        email: formData.email,
        phone: formData.phone,
      })
      user = await api.get(`/api/users/lookup?${params}`)
    } catch {
      user = await api.post('/api/users', {
        first_name: formData.firstName,
        last_name: formData.lastName,
        salutation: formData.salutation,
        email: formData.email,
        phone: formData.phone,
        zelle_refund: formData.zelleRefund,
        zelle_refund_other: formData.zelleRefundOther || null,
      })
    }

    // 2. 解析取貨時間
    let pickupTime = null
    if (formData.estimatedPickup) {
      const parts = formData.estimatedPickup.match(/(\d+)\/(\d+)\/(\d+)\s+(\d+):(\d+)/)
      if (parts) {
        pickupTime = new Date(+parts[3], +parts[1] - 1, +parts[2], +parts[4], +parts[5]).toISOString()
      }
    }

    // 3. 建立訂單
    const i18n = useI18nStore()
    let order
    try {
      order = await api.post('/api/orders', {
        user_id: user.id,
        pickup_time: pickupTime,
        items: cartItems.map(i => ({ product_id: i.id, price: i.price })),
        locale: i18n.locale,
      })
    } catch (err) {
      if (err.status === 409 && err.detail?.duplicate_product_ids) {
        const dupError = new Error('duplicate')
        dupError.duplicateProductIds = err.detail.duplicate_product_ids
        throw dupError
      }
      throw err
    }
    orders.value.push(order)
    return order
  }

  async function fetchOrdersByUser(userId) {
    const result = await api.get(`/api/orders/user/${userId}`)
    orders.value = result
    return result
  }

  async function cancelOrderItem(itemId) {
    await api.put(`/api/orders/items/${itemId}/cancel`)
    for (const order of orders.value) {
      const item = order.items?.find(i => i.id === itemId)
      if (item) {
        item.status = 'cancelled'
        break
      }
    }
  }

  async function updatePickupTime(orderId, isoTimeStr) {
    const updated = await api.put(`/api/orders/${orderId}/pickup_time`, { pickup_time: isoTimeStr })
    const idx = orders.value.findIndex(o => o.id === orderId)
    if (idx !== -1) orders.value[idx] = updated
    return updated
  }

  // 保留介面相容性，waiting list 功能需後端另行實作
  function getWaitingList() { return [] }

  return { orders, createOrder, fetchOrdersByUser, cancelOrderItem, updatePickupTime, getWaitingList }
})
