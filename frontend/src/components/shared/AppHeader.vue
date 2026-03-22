<!--
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-21 21:55:35
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-22 16:11:19
 * @FilePath: \homefinds\frontend\src\components\shared\AppHeader.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <header class="site-header">
    <div class="header-top">
      <h1 class="site-title">Christy's Home Finds</h1>
    </div>
    <div class="nav-row">
      <nav class="nav-tabs">
        <RouterLink class="nav-tab" :class="{ active: route.name === 'shop' }" to="/">
          {{ i18n.t('nav.shop') }}
        </RouterLink>
        <RouterLink class="nav-tab" :class="{ active: route.name === 'rent' }" to="/rent">
          {{ i18n.t('nav.rent') }}
        </RouterLink>
        <RouterLink class="nav-tab" :class="{ active: route.name === 'orders' }" to="/orders">
          {{ i18n.t('nav.orders') }}
        </RouterLink>
        <RouterLink v-if="isAdmin" class="nav-tab" :class="{ active: route.name === 'admin' }" to="/admin">
          {{ i18n.t('nav.admin') }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18nStore } from '@/stores/i18n'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const i18n = useI18nStore()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.currentUser?.is_admin === 1)
</script>

<style scoped>
.site-header {
  background: #ffffffad;
  padding: 14px 0 0 0;
  position: sticky; top: 0; z-index: 100;
  box-shadow: 1px 1px 7px #cccccc;
}
.header-top {
  display: flex; align-items: center; justify-content: center;
  position: relative; margin-bottom: 4px;
}
.site-title {
  font-family: var(--font-display);
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-align: center;
  color: var(--charcoal);
}
.nav-tabs {
  display: flex; width: 100%;
}
.nav-tab {
  font-family: var(--font-body);
  font-size: 0.85rem;
  font-weight: 500;
  padding: 3px 12px 0px 12px;
  background: hsl(161 20% 53% / 1);
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  flex: 1;
  text-align: center;
}
.nav-tab.active {
  color: #fff;
  border-bottom: 3px solid white;
}
.nav-tab:hover:not(.active) {  background: hsl(161deg 20% 53% / 17%); color: black; }

/* nav-row wrapper */
.nav-row { display: flex; align-items: center; gap: 6px; }
.nav-row .nav-tabs { flex: 1; }
</style>
