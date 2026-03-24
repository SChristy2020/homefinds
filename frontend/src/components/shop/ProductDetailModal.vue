<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">{{ i18n.t('productDetail.title') }}</h2>

    <!-- Image Gallery -->
    <div class="gallery">
      <div class="gallery-main">
        <template v-if="images.length">
          <Carousel v-model="current" :wrap-around="true" snap-align="center" class="gallery-carousel">
            <Slide v-for="(img, i) in images" :key="i">
              <img :src="img.url" :alt="product.name" class="gallery-main-img" />
            </Slide>
          </Carousel>
        </template>
        <div v-else class="gallery-placeholder" />
      </div>
      <div
        v-if="images.length > 1"
        class="gallery-thumbs"
        ref="thumbsEl"
        @mousedown="onThumbDragStart"
        @mousemove="onThumbDragMove"
        @mouseup="onThumbDragEnd"
        @mouseleave="onThumbDragEnd"
      >
        <img
          v-for="(img, i) in images"
          :key="i"
          :src="img.url"
          :alt="product.name"
          class="gallery-thumb"
          :class="{ active: i === current }"
          @click="onThumbClick(i)"
        />
      </div>
    </div>

    <!-- Product name -->
    <h3 class="product-name">{{ product.name }}</h3>

    <!-- Category + Code -->
    <div class="badge-row">
      <span v-if="categoryLabel" class="category-badge">{{ categoryLabel }}</span>
      <span v-if="product.code" class="code-badge">#{{ product.code }}</span>
    </div>

    <!-- Status + Pickup time -->
    <div class="status-row">
      <span class="status-dot" :class="`dot-${product.status}`" />
      <span class="status-label">{{ i18n.t(`productDetail.status_${product.status}`) }}</span>
      <span class="pickup-time">
        <template v-if="product.pickupTime">{{ i18n.t('productDetail.availableFrom') }}{{ i18n.t('productDetail.availableStarting') }}{{ formatPickupTime(product.pickupTime) }}</template>
        <template v-else>{{ i18n.t('productDetail.availableFrom') }}{{ i18n.t('productDetail.availableAnytime') }}</template>
      </span>
    </div>

    <!-- Price -->
    <div class="price-row">
      <span v-if="product.originalPrice" class="price-original">${{ product.originalPrice }}</span>
      <span class="price-current">${{ product.price }}</span>
    </div>

    <!-- Add to cart -->
    <button
      class="btn-add-cart"
      :disabled="cart.has(product.id) || product.soldOut"
      @click="handleAddToCart"
    >
      {{ cart.has(product.id) ? i18n.t('productDetail.added') : i18n.t('productDetail.addCart') }}
    </button>

    <!-- Description -->
    <div v-if="product.description" class="description-box" v-html="product.description"></div>

    <!-- Listed date -->
    <div class="listed-date">{{ i18n.t('productDetail.listedOn') }}{{ product.date }}</div>

    <!-- Waiting list -->
    <div class="waiting-section">
      <div class="waiting-title">{{ i18n.t('productDetail.waitingList') }}</div>
      <template v-if="waitingList.length === 0">
        <p class="waiting-empty">{{ i18n.t('productDetail.noWaiting') }}</p>
      </template>
      <template v-else>
        <div v-for="(entry, i) in waitingList" :key="i" class="waiting-item">
          {{ i + 1 }}. {{ entry.last_name }} &nbsp; {{ maskPhone(entry.phone) }} &nbsp; {{ maskEmail(entry.email) }}
        </div>
      </template>
      <ul class="mechanism-list">
        <li v-for="(item, i) in i18n.t('productDetail.mechanism')" :key="i" v-html="item" />
      </ul>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref, computed } from 'vue'

const thumbsEl = ref(null)
const thumbDragging = ref(false)
const thumbDragStartX = ref(0)
const thumbDragScrollLeft = ref(0)
const thumbDragMoved = ref(false)

function onThumbDragStart(e) {
  thumbDragging.value = true
  thumbDragMoved.value = false
  thumbDragStartX.value = e.pageX - thumbsEl.value.offsetLeft
  thumbDragScrollLeft.value = thumbsEl.value.scrollLeft
}
function onThumbDragMove(e) {
  if (!thumbDragging.value) return
  const x = e.pageX - thumbsEl.value.offsetLeft
  const walk = x - thumbDragStartX.value
  if (Math.abs(walk) > 4) thumbDragMoved.value = true
  thumbsEl.value.scrollLeft = thumbDragScrollLeft.value - walk
}
function onThumbDragEnd() {
  thumbDragging.value = false
}
function onThumbClick(i) {
  if (!thumbDragMoved.value) current.value = i
}
import { Carousel, Slide } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'
import BaseModal from '@/components/shared/BaseModal.vue'
import { useCartStore } from '@/stores/cart'
import { useToastStore } from '@/stores/toast'
import { useI18nStore } from '@/stores/i18n'
import { useProductsStore } from '@/stores/products'

const props = defineProps({ modelValue: Boolean, product: Object })
defineEmits(['update:modelValue'])

const cart = useCartStore()
const toast = useToastStore()
const i18n = useI18nStore()
const productsStore = useProductsStore()

const images = computed(() => props.product?.images || [])
const current = ref(0)

const waitingList = computed(() => props.product?.waitingList || [])

const categoryLabel = computed(() => {
  const cat = productsStore.categories.find(c => {
    const enName = c.translations?.find(t => t.locale === 'en')?.name || c.code_prefix
    return enName === props.product?.category
  })
  if (!cat) return props.product?.category || ''
  return cat.translations?.find(t => t.locale === i18n.locale)?.name
    || cat.translations?.find(t => t.locale === 'en')?.name
    || cat.code_prefix
})


function handleAddToCart() {
  cart.add(props.product)
  toast.show(i18n.t('productDetail.addedToast', { name: props.product.name }))
}

function formatPickupTime(dt) {
  if (!dt) return ''
  const d = new Date(dt)
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
}

function maskPhone(phone) {
  if (!phone) return ''
  const str = String(phone)
  if (str.length <= 3) return str
  return '*'.repeat(str.length - 3) + str.slice(-3)
}

function maskEmail(email) {
  if (!email) return ''
  const [local, domain] = email.split('@')
  const maskedLocal = local.slice(0, 3) + '*'.repeat(Math.max(0, local.length - 3))
  const maskedDomain = domain
    ? domain.slice(0, 3) + '*'.repeat(Math.max(0, domain.length - 3))
    : '***'
  return maskedLocal + '@' + maskedDomain
}
</script>

<style scoped>
.modal-title {
  font-family: var(--font-display);
  font-size: 1.1rem; font-weight: 600;
  margin-bottom: 4px;
}

/* Gallery */
.gallery { margin-bottom: 16px; }
.gallery-main {
  position: relative;
  width: 100%; aspect-ratio: 1/1;
  background: #3a3a3a;
  border-radius: var(--radius);
  overflow: hidden;
}
.gallery-carousel {
  width: 100%; height: 100%;
}
.gallery-main-img {
  width: 100%; height: 100%;
  object-fit: cover; display: block;
}
.gallery-placeholder { width: 100%; height: 100%; background: #3a3a3a; }
.gallery-thumbs {
  display: flex; gap: 6px; margin-top: 8px;
  overflow-x: auto; flex-wrap: nowrap;
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
  padding-bottom: 4px;
  cursor: grab;
  user-select: none;
}
.gallery-thumbs:active { cursor: grabbing; }
.gallery-thumbs::-webkit-scrollbar { height: 4px; }
.gallery-thumbs::-webkit-scrollbar-track { background: transparent; }
.gallery-thumbs::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.gallery-thumb {
  width: 60px; height: 60px; flex-shrink: 0;
  object-fit: cover; border-radius: 4px;
  cursor: pointer; opacity: 0.65;
  transition: opacity 0.15s;
  border: 2px solid transparent;
}
.gallery-thumb.active, .gallery-thumb:hover { opacity: 1; border-color: var(--charcoal); }

/* Product name */
.product-name {
  font-size: 1.3rem; font-weight: 700;
  color: var(--charcoal); margin-bottom: 10px;
}

/* Badges */
.badge-row {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.category-badge {
  font-size: .9rem;
  padding: 3px 12px;
  border-radius: 999px;
  color: var(--white);
  background: var(--button)
}
.code-badge {
  font-size: 0.75rem; padding: 3px 10px;
  border: 1.5px solid var(--border);
  border-radius: 999px; color: var(--mid);
}

/* Status + Pickup time */
.status-row {
  display: flex; align-items: center; gap: 6px;
  font-size: 1rem; margin-bottom: 8px; padding: 0 0 0 4px;
}
.status-dot {
  display: inline-block; width: 8px; height: 8px;
  border-radius: 50%; flex-shrink: 0;
}
.dot-available { background: #4caf50; }
.dot-reserved  { background: #ff9800; }
.dot-sold      { background: #f44336; }
.status-label  { color: var(--charcoal); }
.pickup-time   { margin-left: auto; color: var(--charcoal); font-size: 1rem; }

/* Price */
.price-row {
  display: flex; align-items: baseline; gap: 8px;
  margin-bottom: 12px;
}
.price-original {
  font-size: 1.2rem; color: var(--accent);
  text-decoration: line-through;
}
.price-current {
  font-size: 1.4rem; font-weight: 700; color: var(--charcoal);
}

/* Add to cart button */
.btn-add-cart {
  width: 100%; padding: 12px;
  background: var(--accent); color: #fff;
  border: none; border-radius: var(--radius);
  font-size: 0.9rem; font-family: var(--font-body);
  cursor: pointer; margin-bottom: 14px;
  transition: opacity 0.15s;
}
.btn-add-cart:disabled { opacity: 0.45; cursor: not-allowed; }
.btn-add-cart:not(:disabled):hover { opacity: 0.85; }

/* Description */
.description-box {
  font-size: 0.9rem; color: var(--charcoal);
  margin-bottom: 8px;
  line-height: 1.55;
}
.description-box :deep(ul),
.description-box :deep(ol) { padding-left: 1.5em; margin: 0.4em 0; }
.description-box :deep(ul) { list-style-type: disc; }
.description-box :deep(ol) { list-style-type: decimal; }
.description-box :deep(li) { margin: 0.2em 0; }
.description-box :deep(strong) { font-weight: 700; }
.description-box :deep(em) { font-style: italic; }
.description-box :deep(a) { color: var(--accent, #b5935a); text-decoration: underline; }

/* Listed date */
.listed-date {
  font-size: 0.75rem; color: var(--accent);
  margin-bottom: 16px;
}

/* Waiting list */
.waiting-section {
  padding-top: 14px;
  border-top: 1.5px solid var(--border);
}
.waiting-title {
  font-size: 1rem; font-weight: 700;
  color: var(--charcoal); margin-bottom: 6px;
}
.waiting-empty {
  font-size: 0.82rem; color: var(--mid);
  margin-bottom: 10px;
}
.waiting-item {
  font-size: 0.78rem; color: var(--mid); padding: 3px 0;
}
.mechanism-list {
  margin: 10px 0 0 0; padding-left: 18px;
  font-size: 0.9rem; color: var(--charcoal); line-height: 1.7;
  border-top: 1.5px solid var(--border);
  padding-top: 10px;
}
.mechanism-list li { margin-bottom: 2px; }
</style>
