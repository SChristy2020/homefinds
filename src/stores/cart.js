// stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const showModal = ref(false)

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
