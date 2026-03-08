<template>
  <div class="product-card" :class="{ 'sold-out': product.soldOut }">
    <div class="product-img" @click.stop>
      <template v-if="images.length">
        <img :src="images[current].url" :alt="product.name" class="product-img-photo" @click="$emit('open')" />
        <button v-if="images.length > 1" class="img-nav img-prev" @click.stop="prev">&#8249;</button>
        <button v-if="images.length > 1" class="img-nav img-next" @click.stop="next">&#8250;</button>
        <div v-if="images.length > 1" class="img-dots">
          <span v-for="(_, i) in images" :key="i" class="img-dot" :class="{ active: i === current }" @click.stop="current = i" />
        </div>
      </template>
      <div v-else class="product-img-placeholder" @click="$emit('open')"><Home :size="28" /></div>
    </div>
    <div class="product-info" @click="$emit('open')">
      <div class="product-name">{{ product.name }}</div>
      <div class="product-price-row">
        <span v-if="product.originalPrice" class="price-original">${{ product.originalPrice }}</span>
        <span class="price-current">${{ product.price }}</span>
      </div>
      <div class="product-date">{{ product.date }}</div>
      <span v-if="product.soldOut" class="sold-badge">{{ i18n.t('shop.soldOut') }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Home } from 'lucide-vue-next'
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({ product: Object })
defineEmits(['open'])
const i18n = useI18nStore()

const images = computed(() => props.product.images || [])
const current = ref(0)

function prev() {
  current.value = (current.value - 1 + images.value.length) % images.value.length
}
function next() {
  current.value = (current.value + 1) % images.value.length
}
</script>

<style scoped>
.product-card {
  background: var(--warm-white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.18s;
}
.product-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); }
.product-card.sold-out { opacity: 0.5; pointer-events: none; }
.product-img {
  position: relative;
  width: 100%; aspect-ratio: 1;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
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
.img-nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  background: rgba(0,0,0,0.45); color: #fff;
  border: none; cursor: pointer;
  width: 28px; height: 28px; border-radius: 50%;
  font-size: 1.1rem; line-height: 1;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity 0.2s;
  z-index: 2;
}
.product-img:hover .img-nav { opacity: 1; }
.img-prev { left: 6px; }
.img-next { right: 6px; }
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
.product-name  { font-size: 0.78rem; color: var(--mid); margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.product-price-row { display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap; }
.price-original { font-size: 0.73rem; color: var(--light); text-decoration: line-through; }
.price-current  { font-size: 0.95rem; font-weight: 600; color: var(--charcoal); }
.product-date   { font-size: 0.7rem; color: var(--light); margin-top: 2px; }
.sold-badge {
  display: inline-block; font-size: 0.65rem;
  background: var(--red); color: #fff;
  padding: 2px 6px; border-radius: 2px; margin-top: 2px;
}
</style>
