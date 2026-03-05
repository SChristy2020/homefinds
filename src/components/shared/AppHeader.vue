<template>
  <header class="site-header">
    <h1 class="site-title">Christy's Home Finds</h1>
    <nav class="nav-tabs">
      <RouterLink class="nav-tab" :class="{ active: route.name === 'shop' }" to="/">
        Shop
      </RouterLink>
      <RouterLink class="nav-tab" :class="{ active: route.name === 'rent' }" to="/rent">
        Room for Rent
      </RouterLink>
      <RouterLink class="nav-tab" :class="{ active: route.name === 'orders' }" to="/orders">
        My Orders
      </RouterLink>
    </nav>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped>
.site-header {
  background: var(--warm-white);
  border-bottom: 1.5px solid var(--border);
  padding: 18px 40px 0;
  position: sticky; top: 0; z-index: 100;
}
.site-title {
  font-family: var(--font-display);
  font-size: 1.7rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-align: center;
  color: var(--charcoal);
  margin-bottom: 14px;
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
