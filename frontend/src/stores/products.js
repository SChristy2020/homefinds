// stores/products.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useProductsStore = defineStore('products', () => {
  const products = ref([
    { id: 1,  name: '多功能 Blender',   category: 'Kitchen',    price: 15, originalPrice: 30, date: '2026/3/6',  soldOut: false },
    { id: 2,  name: '床頭燈',           category: 'Bedroom',    price: 20, originalPrice: null, date: '2026/3/6', soldOut: false },
    { id: 3,  name: '浴室收納架',       category: 'Bathroom',   price: 35, originalPrice: null, date: '2026/3/8', soldOut: false },
    { id: 4,  name: '廚房計時器',       category: 'Kitchen',    price: 1,  originalPrice: 15,  date: '2026/3/6',  soldOut: false },
    { id: 5,  name: '枕頭組',           category: 'Bedroom',    price: 25, originalPrice: null, date: '2026/3/10', soldOut: false },
    { id: 6,  name: '沐浴組合',         category: 'Bathroom',   price: 18, originalPrice: null, date: '2026/3/12', soldOut: false },
    { id: 7,  name: '桌上收納盒',       category: 'Home & Misc',price: 10, originalPrice: null, date: '2026/3/9',  soldOut: false },
    { id: 8,  name: '床單組',           category: 'Bedroom',    price: 40, originalPrice: 60,  date: '2026/3/7',  soldOut: false },
    { id: 9,  name: '咖啡杯組',         category: 'Kitchen',    price: 12, originalPrice: null, date: '2026/3/11', soldOut: false },
    { id: 10, name: '香氛蠟燭',         category: 'Home & Misc',price: 8,  originalPrice: null, date: '2026/3/13', soldOut: false },
  ])

  const categories = ['Bedroom', 'Kitchen', 'Bathroom', 'Home & Misc']

  function getByCategory(category) {
    if (!category) return products.value
    return products.value.filter(p => p.category === category)
  }

  function search(query) {
    if (!query.trim()) return products.value
    return products.value.filter(p =>
      p.name.toLowerCase().includes(query.toLowerCase())
    )
  }

  function markSoldOut(productId) {
    const p = products.value.find(p => p.id === productId)
    if (p) p.soldOut = true
  }

  return { products, categories, getByCategory, search, markSoldOut }
})
