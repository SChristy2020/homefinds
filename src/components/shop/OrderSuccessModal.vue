<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <div class="success-title">預定成功!</div>
    <div class="success-icon">🎁</div>

    <div v-if="order" class="success-info">
      <p><strong>{{ order.firstName }} {{ order.lastName }}</strong></p>
      <p>稱呼: {{ order.salutation }}</p>
      <p>Email: {{ order.email }}</p>
      <p>Phone: {{ order.phone }}</p>
    </div>

    <div class="section-divider"></div>

    <ol class="success-notes">
      <li>你的資訊將匿名呈現在該物品的 waiting list 裡!</li>
      <li>若你不是第一順位，我們將通知你如果你變成第一順位!</li>
      <li>如果你先zelle付款，該物品將會先被標記"已出售"並禁止其他人再預定!</li>
    </ol>
  </BaseModal>
</template>

<script setup>
import BaseModal from '@/components/shared/BaseModal.vue'
defineProps({ modelValue: Boolean, order: Object })
defineEmits(['update:modelValue'])
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
