<template>
  <div class="product-card" :class="{ 'sold-out': product.soldOut }" @click="onCardClick">
    <div class="product-img">
      <template v-if="images.length">
        <Carousel v-model="current" :wrap-around="true" snap-align="center" class="img-carousel" @slide-start="sliding = true" @slide-end="sliding = false">
          <Slide v-for="(img, i) in images" :key="i">
            <img :src="img.url" :alt="product.name" class="product-img-photo" />
          </Slide>
        </Carousel>
        <div v-if="images.length > 1" class="img-dots">
          <span v-for="(_, i) in images" :key="i" class="img-dot" :class="{ active: i === current }" @click.stop="current = i" />
        </div>
      </template>
      <div v-else class="product-img-placeholder"><Home :size="28" /></div>
    </div>
    <div class="product-info">
      <div class="product-name">{{ product.name }}</div>
      <div class="product-price-row">
        <span v-if="product.originalPrice" class="price-original">${{ product.originalPrice }}</span>
        <span class="price-current">${{ product.price }}</span>
      </div>
      <div class="product-date">{{ i18n.t('productDetail.availableFrom') }}{{ formattedDate ? i18n.t('productDetail.availableStarting') : '' }}{{ formattedDate || i18n.t('productDetail.availableAnytime') }}</div>
      <span v-if="product.soldOut" class="sold-badge">{{ i18n.t('shop.soldOut') }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Home } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'
import { Carousel, Slide } from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'

const props = defineProps({ product: Object })
const emit = defineEmits(['open'])
const i18n = useI18nStore()

const images = computed(() => props.product.images || [])
const current = ref(0)
const sliding = ref(false)

function onCardClick() {
  if (sliding.value) return
  window.gtag?.('event', 'select_item', {
    item_name: props.product.name,
    item_category: props.product.category,
  })
  emit('open')
}

const formattedDate = computed(() => {
  const d = props.product.pickup_available_time
  if (!d) return ''
  const [y, m, day] = d.split('-')
  if (!y || !m || !day) return d
  return `${m}/${day.split('T')[0]}/${y}`
})
</script>

<style scoped>
.product-card {
  background: var(--white);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.18s;
  box-shadow: 1px 1px 5px #cccc;
}
.product-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); }
.product-card.sold-out { opacity: 0.5; }
.product-img {
  position: relative;
  width: 100%; aspect-ratio: 1;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.img-carousel {
  width: 100%; height: 100%;
}
.product-img-photo {
  width: 100%; height: 100%;
  object-fit: cover; aspect-ratio: 1;
  display: block;
}
.product-img-placeholder {
  width: 100%; height: 100%;
  background: linear-gradient(135deg, #2a2a2a 0%, #4a4040 100%);
  display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.4);
  aspect-ratio: 1;
}
.img-dots {
  position: absolute; bottom: 6px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 4px; z-index: 2;
}
.img-dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: rgba(255,255,255,0.5); cursor: pointer;
  transition: background 0.2s;
}
.img-dot.active { background: #fff; }
.product-info  { padding: 10px 10px 12px; }
.product-name  { font-size: .95rem; color: var(--accent); margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500;}
.product-price-row { display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap; }
.price-original { font-size: 1rem; color: var(--accent); text-decoration: line-through; }
.price-current  { font-size: 1.2rem; font-weight: 600; color: var(--charcoal); }
.product-date   { font-size: 0.8rem; color: var(--charcoal); margin-top: 2px; }
.sold-badge {
  display: inline-block; font-size: 0.65rem;
  background: var(--red); color: #fff;
  padding: 2px 6px; border-radius: 2px; margin-top: 2px;
}
</style>
