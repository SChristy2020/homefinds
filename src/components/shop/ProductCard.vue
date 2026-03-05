<template>
  <div class="product-card" :class="{ 'sold-out': product.soldOut }">
    <div class="product-img">
      <div class="product-img-placeholder"><span>🏠</span></div>
    </div>
    <div class="product-info">
      <div class="product-name">{{ product.name }}</div>
      <div class="product-price-row">
        <span v-if="product.originalPrice" class="price-original">${{ product.originalPrice }}</span>
        <span class="price-current">${{ product.price }}</span>
      </div>
      <div class="product-date">{{ product.date }}</div>
      <span v-if="product.soldOut" class="sold-badge">已售出</span>
    </div>
  </div>
</template>

<script setup>
defineProps({ product: Object })
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
  width: 100%; aspect-ratio: 1;
  display: flex; align-items: center; justify-content: center;
}
.product-img-placeholder {
  width: 100%; height: 100%;
  background: linear-gradient(135deg, #2a2a2a 0%, #4a4040 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem; opacity: 0.4;
  aspect-ratio: 1;
}
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
