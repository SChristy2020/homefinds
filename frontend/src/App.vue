<template>
  <AppHeader />
  <main class="main-content">
    <RouterView />
  </main>
  <CartBubble v-if="route.name === 'shop'" />
  <LanguageBubble />
  <ToastNotification />
</template>

<script setup>
import { useRoute } from 'vue-router'
import AppHeader from '@/components/shared/AppHeader.vue'
import CartBubble from '@/components/shop/CartBubble.vue'
import LanguageBubble from '@/components/shared/LanguageBubble.vue'
import ToastNotification from '@/components/shared/ToastNotification.vue'

const route = useRoute()
</script>

<style scoped>
.main-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 24px;
}
</style>
