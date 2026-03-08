<template>
  <div>
    <div class="product-grid">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        @open="$emit('select', product)"
      />
    </div>
    <div v-if="products.length === 0" class="empty-state">
      <div class="empty-state-icon">📦</div>
      <p>沒有找到符合的商品</p>
    </div>
  </div>
</template>

<script setup>
import ProductCard from './ProductCard.vue'
defineProps({ products: Array })
defineEmits(['select'])
</script>

<style scoped>
.product-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}
@media (max-width: 900px) { .product-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 600px) { .product-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
