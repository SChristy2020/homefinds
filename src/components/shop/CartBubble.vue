<template>
  <div class="cart-bubble" @click="openCartModal()">
    <span class="cart-icon">🛒</span>
    <span v-if="cart.count > 0" class="cart-count">{{ cart.count }}</span>
  </div>
</template>

<script setup>
import { inject } from 'vue'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()
const openCartModal = inject('openCartModal')
</script>

<style scoped>
.cart-bubble {
  position: fixed; bottom: 32px; right: 32px;
  background: var(--charcoal); color: #fff;
  width: 52px; height: 52px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; box-shadow: var(--shadow-lg);
  transition: transform 0.2s, background 0.2s;
  z-index: 200;
}
.cart-bubble:hover { transform: scale(1.08); background: var(--accent); }
.cart-count {
  position: absolute; top: -4px; right: -4px;
  background: var(--accent); color: #fff;
  font-size: 0.65rem; font-weight: 700;
  width: 18px; height: 18px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  border: 2px solid var(--cream);
}
.cart-icon { font-size: 1.3rem; }
</style>
