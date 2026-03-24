<!--
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-06 00:00:52
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-22 15:07:19
 * @FilePath: \homefinds\frontend\src\components\shop\CartBubble.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="cart-bubble" @click="onCartClick">
    <ShoppingCart :size="22" />
    <span v-if="cart.count > 0" class="cart-count">{{ cart.count }}</span>
  </div>
</template>

<script setup>
import { ShoppingCart } from 'lucide-vue-next'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

function onCartClick() {
  window.gtag?.('event', 'view_cart')
  cart.showModal = true
}
</script>

<style scoped>
.cart-bubble {
  position: fixed; bottom: 32px; right: 32px;
  background: var(--button); color: #fff;
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
.cart-bubble svg { display: block; }
</style>
