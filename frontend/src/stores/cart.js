// stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

const CART_KEY = 'homefinds_cart'

export const useCartStore = defineStore('cart', () => {
  const saved = localStorage.getItem(CART_KEY)
  const items = ref(saved ? JSON.parse(saved) : [])
  const showModal = ref(false)

  watch(items, (val) => {
    localStorage.setItem(CART_KEY, JSON.stringify(val))
  }, { deep: true })

  const total = computed(() => items.value.reduce((s, i) => s + i.price, 0))
  const count = computed(() => items.value.length)

  function add(product) {
    if (!items.value.find(i => i.id === product.id)) {
      items.value.push({ ...product })
    }
  }
  function remove(productId) {
    items.value = items.value.filter(i => i.id !== productId)
  }
  function clear() {
    items.value = []
  }
  function has(productId) {
    return items.value.some(i => i.id === productId)
  }

  return { items, total, count, add, remove, clear, has, showModal }
})
