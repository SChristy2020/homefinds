// stores/products.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/utils/api'
import { useI18nStore } from '@/stores/i18n'

export const useProductsStore = defineStore('products', () => {
  const rawProducts = ref([])
  const categories = ref([])

  const i18n = useI18nStore()

  const products = computed(() =>
    rawProducts.value.map(p => {
      const trans = p.translations || []
      const t = trans.find(t => t.locale === i18n.locale)
        || trans.find(t => t.locale === 'en')
        || {}
      return {
        ...p,
        name: t.name || p.code,
        originalPrice: p.original_price ?? null,
        date: p.listed_date,
        soldOut: p.status === 'sold',
      }
    })
  )

  async function fetchProducts() {
    rawProducts.value = await api.get('/api/products')
  }

  async function fetchCategories() {
    categories.value = await api.get('/api/categories')
  }

  function getByCategory(categoryEnName) {
    if (!categoryEnName) return products.value
    return products.value.filter(p => p.category === categoryEnName)
  }

  function search(query) {
    if (!query.trim()) return products.value
    return products.value.filter(p =>
      p.name.toLowerCase().includes(query.toLowerCase())
    )
  }

  function markSoldOut(productId) {
    const p = rawProducts.value.find(p => p.id === productId)
    if (p) p.status = 'sold'
  }

  return { products, categories, fetchProducts, fetchCategories, getByCategory, search, markSoldOut }
})
