<template>
  <div>
    <!-- Sticky filters + search bar -->
    <div class="shop-sticky-bar" :class="{ 'is-stuck': isStuck }">
      <!-- Filters bar -->
      <div class="shop-filters">
        <div class="category-pills">
          <button
            class="pill"
            :class="{ active: selectedCategories.length === 0 }"
            @click="selectedCategories = []"
          >
            {{ i18n.t('shop.all') }}
          </button>
          <button
            v-for="cat in productsStore.categories"
            :key="cat.id"
            class="pill"
            :class="{ active: selectedCategories.includes(getCatEnName(cat)) }"
            @click="toggleCategory(getCatEnName(cat))"
          >
            {{ getCatLabel(cat) }}
          </button>
        </div>
        <div class="shop-actions">
          <label class="hide-sold-label">
            <input type="checkbox" v-model="hideSold" class="hide-sold-checkbox" />
            {{ i18n.t('shop.hideSold') }}
          </label>
          <button class="icon-btn" @click="searchOpen = !searchOpen"><Search :size="17" /></button>
          <div class="sort-dropdown" ref="sortRef">
            <button class="icon-btn" :class="{ active: sortOption !== '' }" @click="sortOpen = !sortOpen">
              <ArrowUpDown :size="17" />
            </button>
            <Transition name="slide-down">
              <div v-if="sortOpen" class="sort-menu">
                <button
                  v-for="opt in sortOptions"
                  :key="opt.value"
                  class="sort-item"
                  :class="{ active: sortOption === opt.value }"
                  @click="selectSort(opt.value)"
                >{{ opt.label }}</button>
              </div>
            </Transition>
          </div>
        </div>
      </div>

      <!-- Search -->
      <Transition name="slide-down">
        <div v-if="searchOpen" class="search-bar">
          <Search :size="15" class="search-icon" />
          <input v-model="searchQuery" :placeholder="i18n.t('shop.searchPlaceholder')" autofocus />
        </div>
      </Transition>
    </div>

    <!-- Item count -->
    <div class="item-count">{{ i18n.t('shop.itemCount', { count: filteredProducts.length }) }}</div>

    <!-- Grid -->
    <ProductGrid :products="filteredProducts" @select="openProduct" />

    <!-- Modals -->
    <ProductDetailModal
      v-if="selectedProduct"
      v-model="showDetailModal"
      :product="selectedProduct"
    />
    <CartModal v-model="cart.showModal" />
    <OrderSuccessModal v-model="showSuccessModal" :order="lastOrder" />
  </div>
</template>

<script setup>
import { ref, computed, provide, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Search, ArrowUpDown } from 'lucide-vue-next'
import { useProductsStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useI18nStore } from '@/stores/i18n'
import ProductGrid from '@/components/shop/ProductGrid.vue'
import ProductDetailModal from '@/components/shop/ProductDetailModal.vue'
import CartModal from '@/components/shop/CartModal.vue'
import OrderSuccessModal from '@/components/shop/OrderSuccessModal.vue'

const productsStore = useProductsStore()
const cart = useCartStore()
const i18n = useI18nStore()

const selectedCategories = ref([])
const isStuck = ref(false)

function onScrollSticky() {
  isStuck.value = window.scrollY > 10
}

onMounted(async () => {
  await Promise.all([
    productsStore.fetchCategories(),
    productsStore.fetchProducts(),
  ])
  document.addEventListener('click', onClickOutside)
  window.addEventListener('scroll', onScrollSticky, { passive: true })
})

function toggleCategory(enName) {
  const idx = selectedCategories.value.indexOf(enName)
  if (idx === -1) {
    selectedCategories.value.push(enName)
    window.gtag?.('event', 'select_category', { category: enName })
  } else {
    selectedCategories.value.splice(idx, 1)
  }
}

function getCatEnName(cat) {
  return cat.translations?.find(t => t.locale === 'en')?.name || cat.code_prefix
}

function getCatLabel(cat) {
  return cat.translations?.find(t => t.locale === i18n.locale)?.name
    || cat.translations?.find(t => t.locale === 'en')?.name
    || cat.code_prefix
}
const searchOpen = ref(false)
const searchQuery = ref('')
const hideSold = ref(false)
const sortOption = ref('')
const sortOpen = ref(false)
const sortRef = ref(null)

const sortOptions = computed(() => [
  { value: '',           label: i18n.t('shop.sortDefault') },
  { value: 'price_asc',  label: i18n.t('shop.sortPriceLow') },
  { value: 'price_desc', label: i18n.t('shop.sortPriceHigh') },
  { value: 'name_asc',   label: i18n.t('shop.sortNameAsc') },
  { value: 'name_desc',  label: i18n.t('shop.sortNameDesc') },
  { value: 'date_new',   label: i18n.t('shop.sortDateNew') },
  { value: 'date_old',   label: i18n.t('shop.sortDateOld') },
])

function selectSort(value) {
  sortOption.value = value
  sortOpen.value = false
}

function onClickOutside(e) {
  if (sortRef.value && !sortRef.value.contains(e.target)) sortOpen.value = false
}

onUnmounted(() => {
  document.removeEventListener('click', onClickOutside)
  window.removeEventListener('scroll', onScrollSticky)
})

const selectedProduct = ref(null)
const showDetailModal = ref(false)
const showSuccessModal = ref(false)
const lastOrder = ref(null)

provide('onOrderSuccess', (order) => {
  lastOrder.value = order
  showSuccessModal.value = true
})

const filteredProducts = computed(() => {
  let list = selectedCategories.value.length === 0
    ? productsStore.products
    : productsStore.products.filter(p => selectedCategories.value.includes(p.category))
  if (hideSold.value) {
    list = list.filter(p => p.status !== 'sold')
  }
  if (searchQuery.value.trim()) {
    list = list.filter(p => p.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  if (sortOption.value === 'price_asc') return [...list].sort((a, b) => a.price - b.price)
  if (sortOption.value === 'price_desc') return [...list].sort((a, b) => b.price - a.price)
  if (sortOption.value === 'name_asc') return [...list].sort((a, b) => a.name.localeCompare(b.name))
  if (sortOption.value === 'name_desc') return [...list].sort((a, b) => b.name.localeCompare(a.name))
  if (sortOption.value === 'date_new') return [...list].sort((a, b) => new Date(b.date) - new Date(a.date))
  if (sortOption.value === 'date_old') return [...list].sort((a, b) => new Date(a.date) - new Date(b.date))
  const catOrder = Object.fromEntries(
    productsStore.categories.map(c => {
      const enName = c.translations?.find(t => t.locale === 'en')?.name || ''
      return [enName, c.sort_order ?? Infinity]
    })
  )
  return [...list].sort((a, b) => {
    const catA = catOrder[a.category] ?? Infinity
    const catB = catOrder[b.category] ?? Infinity
    if (catA !== catB) return catA - catB
    const sortA = a.sort ?? 0
    const sortB = b.sort ?? 0
    if (sortA !== sortB) return sortA - sortB
    return a.id - b.id
  })
})

function openProduct(product) {
  selectedProduct.value = product
  showDetailModal.value = true
}

// 從 URL query ?product=ID 自動開啟商品跳窗
const route = useRoute()
watch(
  () => productsStore.products,
  (list) => {
    if (!list.length) return
    const pid = Number(route.query.product)
    if (!pid) return
    const found = list.find(p => p.id === pid)
    if (found) openProduct(found)
  },
  { immediate: true }
)

</script>

<style scoped>
.shop-sticky-bar {
  position: sticky;
  top: var(--header-height, 78px);
  z-index: 90;
  margin: -20px -24px 0;
  padding: 10px 24px 6px;
  transition: background 0.2s, box-shadow 0.2s;
}
.shop-sticky-bar.is-stuck {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 10px 6px 1px;
}
.shop-sticky-bar.is-stuck .category-pills {
  flex-wrap: nowrap;
  overflow-x: auto;
  justify-content: flex-start;
  scrollbar-width: none;
  -ms-overflow-style: none;
  width: 100%;
}
.shop-sticky-bar.is-stuck .category-pills::-webkit-scrollbar {
  display: none;
}
.shop-sticky-bar.is-stuck .category-pills .pill {
  flex-shrink: 0;
  white-space: nowrap;
}
.shop-filters {
  display: flex; flex-direction: column; align-items: center;
  margin-bottom: 4px; gap: 6px;
}
.category-pills { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
.pill {
  font-size: 0.78rem; padding: 5px 14px;
  border: 1px solid var(--charcoal); background: transparent;
  border-radius: 999px; cursor: pointer;
  transition: all 0.18s; font-family: var(--font-body);
  letter-spacing: 0.02em; color: var(--charcoal);
}
.pill.active { background: var(--button); border: 1.5px solid var(--button); color: #fff; }
.pill:hover:not(.active) { background: var(--light); }
.shop-actions { display: flex; gap: 12px; align-items: center; }
.hide-sold-label {
  display: flex; align-items: center; gap: 5px;
  font-size: 0.78rem; color: var(--charcoal);
  cursor: pointer; user-select: none;
}
.hide-sold-checkbox {
  appearance: none; -webkit-appearance: none;
  width: 14px; height: 14px; flex-shrink: 0;
  border: 1.5px solid var(--charcoal); border-radius: 3px;
  background: transparent; cursor: pointer;
  display: grid; place-content: center;
  transition: background 0.15s, border-color 0.15s;
}
.hide-sold-checkbox:checked {
  background: var(--button); border-color: var(--button);
}
.hide-sold-checkbox:checked::after {
  content: '';
  width: 4px; height: 7px;
  border: 2px solid #fff;
  border-top: none; border-left: none;
  transform: rotate(45deg) translate(-1px, -1px);
}
.icon-btn {
  background: none; border: none; cursor: pointer;
  color: var(--charcoal); padding: 4px;
  display: flex; align-items: center;
  transition: color 0.15s;
}
.icon-btn:hover { color: var(--accent); }
.icon-btn.active { color: var(--button); }
.sort-dropdown { position: relative; }
.sort-menu {
  position: absolute; right: 0; top: calc(100% + 6px);
  background: var(--accent-light); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  min-width: 140px; z-index: 100; overflow: hidden;
}
.sort-item {
  display: block; width: 100%;
  padding: 8px 14px; text-align: left;
  font-family: var(--font-body); font-size: 0.8rem; color: var(--charcoal);
  background: none; border: none; cursor: pointer;
  transition: background 0.12s;
}
.sort-item:hover { background: var(--border); }
.sort-item.active { color: var(--button); font-weight: 600; }
.search-bar {
  display: flex; gap: 10px; align-items: center;
  background: var(--light-light); border: 1.5px solid var(--border);
  border-radius: var(--radius); padding: 6px 14px; margin-top: 6px;
}
.search-bar input {
  border: none; background: transparent;
  font-family: var(--font-body); font-size: 0.85rem;
  outline: none; flex: 1; color: var(--accent);
}
.search-bar input::placeholder { color: var(--light); }
.search-icon { color: var(--mid); flex-shrink: 0; }
.item-count {
  font-size: 0.82rem; color: var(--mid);
  margin-top: 14px; margin-bottom: 14px;
}
.slide-down-enter-active, .slide-down-leave-active { transition: all 0.2s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
