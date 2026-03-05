<template>
  <div>
    <!-- Filters bar -->
    <div class="shop-filters">
      <div class="category-pills">
        <button
          v-for="cat in productsStore.categories"
          :key="cat"
          class="pill"
          :class="{ active: selectedCategory === cat }"
          @click="selectedCategory = cat"
        >
          {{ i18n.t('shop.categories.' + cat) }}
        </button>
      </div>
      <div class="shop-actions">
        <button class="icon-btn" @click="searchOpen = !searchOpen">🔍</button>
        <button class="icon-btn" @click="toggleSort">↕</button>
      </div>
    </div>

    <!-- Search -->
    <Transition name="slide-down">
      <div v-if="searchOpen" class="search-bar">
        <span>🔍</span>
        <input v-model="searchQuery" :placeholder="i18n.t('shop.searchPlaceholder')" autofocus />
      </div>
    </Transition>

    <!-- Grid -->
    <ProductGrid :products="filteredProducts" @select="openProduct" />

    <!-- Modals -->
    <ProductDetailModal
      v-if="selectedProduct"
      v-model="showDetailModal"
      :product="selectedProduct"
    />
    <CartModal v-model="showCartModal" />
    <OrderSuccessModal v-model="showSuccessModal" :order="lastOrder" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProductsStore } from '@/stores/products'
import { useI18nStore } from '@/stores/i18n'
import ProductGrid from '@/components/shop/ProductGrid.vue'
import ProductDetailModal from '@/components/shop/ProductDetailModal.vue'
import CartModal from '@/components/shop/CartModal.vue'
import OrderSuccessModal from '@/components/shop/OrderSuccessModal.vue'

import { provide } from 'vue'

const productsStore = useProductsStore()
const i18n = useI18nStore()

const selectedCategory = ref('Bedroom')
const searchOpen = ref(false)
const searchQuery = ref('')
const sortAsc = ref(true)

const selectedProduct = ref(null)
const showDetailModal = ref(false)
const showCartModal = ref(false)
const showSuccessModal = ref(false)
const lastOrder = ref(null)

provide('openCartModal', () => { showCartModal.value = true })
provide('onOrderSuccess', (order) => {
  lastOrder.value = order
  showSuccessModal.value = true
})

const filteredProducts = computed(() => {
  let list = productsStore.getByCategory(selectedCategory.value)
  if (searchQuery.value.trim()) {
    list = list.filter(p => p.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  return sortAsc.value ? [...list].sort((a,b) => a.price - b.price) : [...list].sort((a,b) => b.price - a.price)
})

function openProduct(product) {
  selectedProduct.value = product
  showDetailModal.value = true
}

function toggleSort() {
  sortAsc.value = !sortAsc.value
}
</script>

<style scoped>
.shop-filters {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 24px; flex-wrap: wrap; gap: 10px;
}
.category-pills { display: flex; gap: 8px; flex-wrap: wrap; }
.pill {
  font-size: 0.78rem; padding: 5px 14px;
  border: 1.5px solid var(--charcoal); background: transparent;
  border-radius: 999px; cursor: pointer;
  transition: all 0.18s; font-family: var(--font-body);
  letter-spacing: 0.02em;
}
.pill.active { background: var(--charcoal); color: #fff; }
.pill:hover:not(.active) { background: var(--border); }
.shop-actions { display: flex; gap: 12px; align-items: center; }
.icon-btn {
  background: none; border: none; cursor: pointer;
  font-size: 1.1rem; color: var(--charcoal); padding: 4px;
  transition: color 0.15s;
}
.icon-btn:hover { color: var(--accent); }
.search-bar {
  display: flex; gap: 10px; align-items: center;
  background: var(--warm-white); border: 1.5px solid var(--border);
  border-radius: var(--radius); padding: 6px 14px; margin-bottom: 20px;
}
.search-bar input {
  border: none; background: transparent;
  font-family: var(--font-body); font-size: 0.85rem;
  outline: none; flex: 1; color: var(--charcoal);
}
.search-bar input::placeholder { color: var(--light); }
.slide-down-enter-active, .slide-down-leave-active { transition: all 0.2s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
