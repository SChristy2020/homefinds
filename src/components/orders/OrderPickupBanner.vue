<template>
  <div class="pickup-banner">
    <div class="pickup-row">
      <span class="pickup-time">
        {{ i18n.t('orders.pickupTime') }}<strong>{{ order.pickupTime }}</strong>
      </span>
      <button class="btn-notify" @click="$emit('notify')">{{ i18n.t('orders.notifyChristy') }}</button>
    </div>
    <p class="pickup-note">{{ i18n.t('orders.pickupNote') }}</p>
  </div>
</template>

<script setup>
import { useI18nStore } from '@/stores/i18n'
defineProps({ order: Object })
defineEmits(['notify'])
const i18n = useI18nStore()
</script>

<style scoped>
.pickup-banner {
  background: var(--warm-white); border: 1.5px solid var(--border);
  border-radius: var(--radius); padding: 16px 20px; margin-bottom: 20px;
}
.pickup-row { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
.pickup-time { font-size: 0.88rem; }
.pickup-time strong { font-size: 1rem; }
.pickup-note { font-size: 0.78rem; color: var(--mid); margin-top: 6px; }
.btn-notify {
  padding: 7px 16px; background: var(--charcoal); color: #fff;
  border: none; border-radius: var(--radius); font-size: 0.8rem;
  font-family: var(--font-body); cursor: pointer; transition: background 0.18s;
}
.btn-notify:hover { background: var(--accent); }
</style>
