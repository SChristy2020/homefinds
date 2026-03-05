<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-overlay" @click.self="$emit('update:modelValue', false)">
        <div class="modal" :class="size === 'lg' ? 'modal-lg' : ''">
          <button class="modal-close" @click="$emit('update:modelValue', false)">×</button>
          <slot />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  size: { type: String, default: 'md' }, // 'md' | 'lg'
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.45);
  backdrop-filter: blur(2px);
  display: flex; align-items: center; justify-content: center;
  z-index: 300; padding: 20px;
}
.modal {
  background: var(--warm-white);
  border-radius: 6px;
  padding: 32px;
  max-width: 520px; width: 100%;
  max-height: 90vh; overflow-y: auto;
  box-shadow: var(--shadow-lg);
  position: relative;
}
.modal-lg { max-width: 640px; }
.modal-close {
  position: absolute; top: 16px; right: 20px;
  background: none; border: none; font-size: 1.4rem;
  cursor: pointer; color: var(--mid); line-height: 1;
}
.modal-close:hover { color: var(--charcoal); }

.modal-enter-active, .modal-leave-active { transition: all 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-leave-to   { opacity: 0; }
.modal-enter-from :deep(.modal),
.modal-leave-to   :deep(.modal) {
  transform: translateY(20px);
}
</style>
