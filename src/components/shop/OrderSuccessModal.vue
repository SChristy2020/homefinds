<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <div class="success-title">{{ i18n.t('orderSuccess.title') }}</div>
    <div class="success-icon">🎁</div>

    <div v-if="order" class="success-info">
      <p><strong>{{ order.firstName }} {{ order.lastName }}</strong></p>
      <p>{{ i18n.t('orderSuccess.salutation') }}: {{ order.salutation }}</p>
      <p>Email: {{ order.email }}</p>
      <p>Phone: {{ order.phone }}</p>
    </div>

    <div class="section-divider"></div>

    <ol class="success-notes">
      <li>{{ i18n.t('orderSuccess.note1') }}</li>
      <li>{{ i18n.t('orderSuccess.note2') }}</li>
      <li>{{ i18n.t('orderSuccess.note3') }}</li>
    </ol>
  </BaseModal>
</template>

<script setup>
import BaseModal from '@/components/shared/BaseModal.vue'
import { useI18nStore } from '@/stores/i18n'
defineProps({ modelValue: Boolean, order: Object })
defineEmits(['update:modelValue'])
const i18n = useI18nStore()
</script>

<style scoped>
.success-title {
  font-family: var(--font-display);
  font-size: 1.4rem; font-weight: 700;
  text-align: center; margin-bottom: 10px;
}
.success-icon { text-align: center; font-size: 3rem; margin-bottom: 20px; }
.success-info { font-size: 0.83rem; color: var(--mid); margin-bottom: 4px; }
.success-info p { margin-bottom: 3px; }
.success-notes { font-size: 0.8rem; color: var(--mid); padding-left: 16px; }
.success-notes li { margin-bottom: 8px; }
.success-notes li::marker { color: var(--accent); }
</style>
