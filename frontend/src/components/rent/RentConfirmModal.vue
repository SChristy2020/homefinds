<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">{{ i18n.t('rentConfirm.title') }}</h2>
    <p class="text-sm text-muted">
      {{ fmt(selection.start) }} – {{ fmt(selection.end) }}
      &nbsp; {{ i18n.t('rentConfirm.total') }} {{ nights }} {{ nights === 1 ? i18n.t('rentConfirm.night') : i18n.t('rentConfirm.nights') }}
    </p>
    <div class="price-line">${{ totalPrice }} USD</div>

    <UserInfoForm v-model="form" class="mt-16" />

    <div v-if="bookingDescription" class="policy" v-html="bookingDescription"></div>
    <div v-else class="policy">
      <p v-html="i18n.t('rentConfirm.depositNote')"></p>
      <p>{{ i18n.t('rentConfirm.cancelNote') }}</p>
      <p class="mt-8"><strong>{{ i18n.t('rentConfirm.refundPolicy') }}</strong></p>
      <div class="policy-row"><span class="days">14+ days:</span><span>{{ i18n.t('rentConfirm.refund14') }}</span></div>
      <div class="policy-row"><span class="days">7–13 days:</span><span>{{ i18n.t('rentConfirm.refund7') }}</span></div>
      <div class="policy-row"><span class="days">&lt;7 days / no-show:</span><span>{{ i18n.t('rentConfirm.refundLess') }}</span></div>
      <p class="mt-8">{{ i18n.t('rentConfirm.remainingNote') }}</p>
    </div>

    <div style="text-align:right; margin-top:16px;">
      <button class="btn-primary" :disabled="!isValid" @click="handleConfirm">{{ i18n.t('rentConfirm.confirm') }}</button>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseModal from '@/components/shared/BaseModal.vue'
import UserInfoForm from '@/components/shared/UserInfoForm.vue'
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({
  modelValue: Boolean,
  selection: Object,
  nights: Number,
  totalPrice: Number,
  bookingDescription: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue', 'confirmed'])

const i18n = useI18nStore()
const form = ref({ firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '', zelleRefund: 'phone', zelleRefundOther: '' })

const isValid = computed(() =>
  form.value.firstName && form.value.lastName &&
  form.value.email && form.value.phone
)

function fmt(d) {
  if (!d) return ''
  return `${String(d.getMonth()+1).padStart(2,'0')}/${String(d.getDate()).padStart(2,'0')}/${d.getFullYear()}`
}

function handleConfirm() {
  if (!isValid.value) return
  emit('confirmed', { ...form.value })
  form.value = { firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '', zelleRefund: 'phone', zelleRefundOther: '' }
}
</script>

<style scoped>
.modal-title {
  font-family: var(--font-display);
  font-size: 1.25rem; font-weight: 600; margin-bottom: 8px;
}
.price-line { font-size: 1.2rem; font-weight: 700; margin: 8px 0; }
.policy {
  font-size: 0.78rem; color: var(--mid);
  margin-top: 12px; padding-top: 12px;
  border-top: 1.5px solid var(--border);
}
.policy p { margin-bottom: 3px; }
.policy strong { color: var(--charcoal); }
.policy-row { display: flex; gap: 10px; margin-bottom: 2px; }
.days { font-weight: 600; color: var(--charcoal); min-width: 100px; }
</style>
