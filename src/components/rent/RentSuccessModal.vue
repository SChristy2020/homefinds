<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <div class="success-title">Reservation</div>
    <div class="success-icon">📅✅</div>
    <p class="text-sm text-muted text-center">
      {{ fmt(selection.start) }} – {{ fmt(selection.end) }}
      &nbsp; total {{ nights }} nights
    </p>
    <div class="price-line">${{ totalPrice }} USD</div>
    <div v-if="reservation" class="info">
      <p>Name: {{ reservation.firstName }} {{ reservation.lastName }}</p>
      <p>Email: {{ reservation.email }}</p>
      <p>Phone: {{ reservation.phone }}</p>
    </div>
  </BaseModal>
</template>

<script setup>
import BaseModal from '@/components/shared/BaseModal.vue'
defineProps({ modelValue: Boolean, reservation: Object, nights: Number, totalPrice: Number, selection: Object })
defineEmits(['update:modelValue'])

function fmt(d) {
  if (!d) return ''
  return `${d.getMonth()+1}/${d.getDate()}/${String(d.getFullYear()).slice(2)}`
}
</script>

<style scoped>
.success-title {
  font-family: var(--font-display);
  font-size: 1.25rem; font-weight: 600;
  text-align: center; margin-bottom: 10px;
}
.success-icon { text-align: center; font-size: 2.5rem; margin-bottom: 12px; }
.price-line { font-size: 1.1rem; font-weight: 700; text-align: center; margin: 8px 0 16px; }
.info { font-size: 0.83rem; color: var(--mid); }
.info p { margin-bottom: 3px; }
</style>
