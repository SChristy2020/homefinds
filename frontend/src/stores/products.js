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
        images: (p.images || []).map(img => ({ ...img, url: img.name ? `${import.meta.env.VITE_IMAGE_BASE_URL}${img.name}` : img.url })),
        name: t.name || p.code,
        description: t.description || '',
        originalPrice: p.original_price ?? null,
        date: p.listed_date,
        pickupTime: p.pickup_available_time || null,
        soldOut: p.status === 'sold',
        waitingList: (p.waiting_list_summary || []).filter(e => !e.is_cancelled),
      }
    })
  )

  async function fetchProducts() {
    rawProducts.value = await api.get('/api/products?visible_only=true')
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
