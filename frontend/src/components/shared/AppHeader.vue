<template>
  <header class="site-header">
    <div class="header-top">
      <h1 class="site-title">Christy's Home Finds</h1>
    </div>
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
    </nav>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useI18nStore } from '@/stores/i18n'

const route = useRoute()
const i18n = useI18nStore()
</script>

<style scoped>
.site-header {
  background: var(--warm-white);
  border-bottom: 1.5px solid var(--border);
  padding: 14px 40px 0;
  position: sticky; top: 0; z-index: 100;
}
.header-top {
  display: flex; align-items: center; justify-content: center;
  position: relative; margin-bottom: 14px;
}
.site-title {
  font-family: var(--font-display);
  font-size: 1.7rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-align: center;
  color: var(--charcoal);
}
.nav-tabs {
  display: flex; gap: 4px; justify-content: center;
}
.nav-tab {
  font-family: var(--font-body);
  font-size: 0.85rem;
  font-weight: 500;
  padding: 8px 24px;
  border: 1.5px solid var(--charcoal);
  background: transparent;
  color: var(--charcoal);
  cursor: pointer;
  border-radius: 2px 2px 0 0;
  border-bottom: none;
  transition: all 0.2s;
  letter-spacing: 0.03em;
  text-decoration: none;
}
.nav-tab.active {
  background: var(--charcoal);
  color: #fff;
}
.nav-tab:hover:not(.active) { background: var(--border); }
</style>
