<!--
 * @Author: Christy qsa8647332@gmail.com
 * @Date: 2026-03-21 23:47:06
 * @LastEditors: Christy qsa8647332@gmail.com
 * @LastEditTime: 2026-03-22 14:25:06
 * @FilePath: \homefinds\frontend\src\components\shared\BaseModal.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-overlay" @click.self="!noBackdropClose && $emit('update:modelValue', false)">
        <div class="modal" :class="size === 'xl' ? 'modal-xl' : size === 'lg' ? 'modal-lg' : ''">
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
  size: { type: String, default: 'md' }, // 'md' | 'lg' | 'xl'
  noBackdropClose: { type: Boolean, default: false },
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
  max-height: 80vh; overflow-y: auto;
  box-shadow: var(--shadow-lg);
  position: relative;
}
.modal-lg { max-width: 640px; }
.modal-xl { max-width: 900px; }
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
