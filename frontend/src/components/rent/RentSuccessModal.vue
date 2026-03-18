<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <div class="success-title">{{ i18n.t('rentSuccess.title') }}</div>
    <div class="success-icon"><CalendarCheck :size="48" /></div>
    <p class="text-sm text-muted text-center">
      {{ fmt(selection.start) }} – {{ fmt(selection.end) }}
      &nbsp; {{ i18n.t('rentSuccess.total') }} {{ nights }} {{ i18n.t('rentSuccess.nights') }}
    </p>
    <div class="price-line">${{ totalPrice }} USD</div>
    <div v-if="reservation" class="info">
      <p v-if="reservation.orderNumber" class="order-no">{{ reservation.orderNumber }}</p>
      <p>{{ i18n.t('rentSuccess.name') }}: {{ reservation.firstName }} {{ reservation.lastName }}</p>
      <p>{{ i18n.t('rentSuccess.email') }}: {{ reservation.email }}</p>
      <p>{{ i18n.t('rentSuccess.phone') }}: {{ reservation.phone }}</p>
    </div>
  </BaseModal>
</template>

<script setup>
import { CalendarCheck } from 'lucide-vue-next'
import BaseModal from '@/components/shared/BaseModal.vue'
import { useI18nStore } from '@/stores/i18n'
defineProps({ modelValue: Boolean, reservation: Object, nights: Number, totalPrice: Number, selection: Object })
defineEmits(['update:modelValue'])
const i18n = useI18nStore()

function fmt(d) {
  if (!d) return ''
  return `${String(d.getMonth()+1).padStart(2,'0')}/${String(d.getDate()).padStart(2,'0')}/${d.getFullYear()}`
}
</script>

<style scoped>
.success-title {
  font-family: var(--font-display);
  font-size: 1.25rem; font-weight: 600;
  text-align: center; margin-bottom: 10px;
}
.success-icon { display: flex; justify-content: center; color: var(--accent); margin-bottom: 12px; }
.price-line { font-size: 1.1rem; font-weight: 700; text-align: center; margin: 8px 0 16px; }
.info { font-size: 0.83rem; color: var(--mid); }
.info p { margin-bottom: 3px; }
.order-no { font-size: 1rem; font-weight: 700; color: var(--charcoal); letter-spacing: 0.05em; margin-bottom: 8px; }
</style>
