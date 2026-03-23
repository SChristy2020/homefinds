<!--
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-09 23:46:03
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-22 20:38:16
 * @FilePath: \homefinds\frontend\src\App.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <AppHeader />
  <main class="main-content">
    <RouterView />
  </main>
  <CartBubble v-if="route.name === 'shop'" />
  <GuideBubble />
  <LanguageBubble />
  <ToastNotification />
</template>

<script setup>
import { useRoute } from 'vue-router'
import AppHeader from '@/components/shared/AppHeader.vue'
import CartBubble from '@/components/shop/CartBubble.vue'
import LanguageBubble from '@/components/shared/LanguageBubble.vue'
import GuideBubble from '@/components/shared/GuideBubble.vue'
import ToastNotification from '@/components/shared/ToastNotification.vue'

const route = useRoute()
</script>

<style scoped>
.main-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 24px;
}
</style>
