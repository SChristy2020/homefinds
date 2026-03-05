<template>
  <Transition name="toast">
    <div v-if="toast.message" class="toast">{{ toast.message }}</div>
  </Transition>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'
const toast = useToastStore()
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--charcoal);
  color: #fff;
  padding: 10px 24px;
  border-radius: 99px;
  font-size: 0.82rem;
  font-weight: 500;
  z-index: 500;
  pointer-events: none;
  white-space: nowrap;
}
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(-50%) translateY(10px); }
.toast-leave-to   { opacity: 0; transform: translateX(-50%) translateY(-6px); }
</style>
