// stores/orders.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref([])        // shop orders
  const waitingLists = ref({})  // { productId: [{ lastName, phone, email }] }

  function addOrder(orderData, cartItems) {
    const order = {
      id: Date.now(),
      ...orderData,
      items: cartItems.map(i => ({ ...i })),
      pickupTime: orderData.estimatedPickup || '',
      createdAt: new Date(),
    }
    orders.value.push(order)

    // Register each item in waiting list and record position
    order.items.forEach(item => {
      if (!waitingLists.value[item.id]) waitingLists.value[item.id] = []
      waitingLists.value[item.id].push({
        lastName: orderData.lastName,
        phone: orderData.phone,
        email: orderData.email,
      })
      item.waitingPosition = waitingLists.value[item.id].length
    })
    return order
  }

  function cancelItem(orderId, productId) {
    const order = orders.value.find(o => o.id === orderId)
    if (!order) return
    order.items = order.items.filter(i => i.id !== productId)
    if (waitingLists.value[productId]) {
      waitingLists.value[productId] = waitingLists.value[productId]
        .filter(e => e.email !== order.email)
    }
  }

  function findOrder(lastName, email, phone) {
    if (!lastName || !email || !phone) return null
    return orders.value.find(o =>
      o.lastName.toLowerCase() === lastName.toLowerCase() &&
      o.email.toLowerCase() === email.toLowerCase() &&
      o.phone === phone
    ) || null
  }

  function getWaitingList(productId) {
    return waitingLists.value[productId] || []
  }

  return { orders, waitingLists, addOrder, cancelItem, findOrder, getWaitingList }
})
