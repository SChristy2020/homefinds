<template>
  <div>
    <div class="form-row">
      <div class="form-group">
        <label>{{ i18n.t('userForm.firstName') }}</label>
        <input :value="modelValue.firstName" :placeholder="i18n.t('userForm.firstName')" @input="update('firstName', $event.target.value)" />
      </div>
      <div class="form-group">
        <label>{{ i18n.t('userForm.lastName') }}</label>
        <input :value="modelValue.lastName" :placeholder="i18n.t('userForm.lastName')" @input="update('lastName', $event.target.value)" />
      </div>
    </div>
    <div class="form-group">
      <label>{{ i18n.t('userForm.salutation') }}</label>
      <div class="radio-group">
        <label><input type="radio" :checked="modelValue.salutation === 'Mr.'" @change="update('salutation', 'Mr.')" /> Mr.</label>
        <label><input type="radio" :checked="modelValue.salutation === 'Miss'" @change="update('salutation', 'Miss')" /> Miss</label>
      </div>
    </div>
    <div class="form-group">
      <label>Email</label>
      <input :value="modelValue.email" type="email" placeholder="your@email.com" @input="update('email', $event.target.value)" />
    </div>
    <div class="form-group">
      <label>{{ i18n.t('userForm.phone') }}</label>
      <input :value="modelValue.phone" :placeholder="i18n.t('userForm.phonePlaceholder')" @input="update('phone', $event.target.value)" />
    </div>
  </div>
</template>

<script setup>
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({ modelValue: Object })
const emit = defineEmits(['update:modelValue'])
const i18n = useI18nStore()

function update(field, value) {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}
</script>
