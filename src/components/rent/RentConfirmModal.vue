<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">Reservation</h2>
    <p class="text-sm text-muted">
      {{ fmt(selection.start) }} – {{ fmt(selection.end) }}
      &nbsp; total {{ nights }} night{{ nights > 1 ? 's' : '' }}
    </p>
    <div class="price-line">${{ totalPrice }} USD</div>

    <div class="form-row mt-16">
      <div class="form-group">
        <label>First Name</label>
        <input v-model="form.firstName" placeholder="First Name" />
      </div>
      <div class="form-group">
        <label>Last Name</label>
        <input v-model="form.lastName" placeholder="Last Name" />
      </div>
    </div>
    <div class="form-group">
      <label>稱呼</label>
      <div class="radio-group">
        <label><input type="radio" v-model="form.salutation" value="Mr." /> Mr.</label>
        <label><input type="radio" v-model="form.salutation" value="Miss" /> Miss</label>
      </div>
    </div>
    <div class="form-group">
      <label>Email</label>
      <input v-model="form.email" type="email" placeholder="your@email.com" />
    </div>
    <div class="form-group">
      <label>Phone</label>
      <input v-model="form.phone" placeholder="(xxx)xxx-xxxx" />
    </div>

    <div class="policy">
      <p>請支付 <strong>30%</strong> 租金以完成預定！並在 note 填上你的名字。</p>
      <p>若1日內未付款，預定將取消。</p>
      <p class="mt-8"><strong>取消預定的訂金退款政策</strong></p>
      <div class="policy-row"><span class="days">14+ days:</span><span>80% refund</span></div>
      <div class="policy-row"><span class="days">7–13 days:</span><span>50% refund</span></div>
      <div class="policy-row"><span class="days">&lt;7 days / no-show:</span><span>non-refundable</span></div>
      <p class="mt-8">請於入住時繳交剩餘 70% 訂金。</p>
    </div>

    <div style="text-align:right; margin-top:16px;">
      <button class="btn-primary" :disabled="!isValid" @click="handleConfirm">Confirm</button>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseModal from '@/components/shared/BaseModal.vue'

const props = defineProps({
  modelValue: Boolean,
  selection: Object,
  nights: Number,
  totalPrice: Number,
})
const emit = defineEmits(['update:modelValue', 'confirmed'])

const form = ref({ firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '' })

const isValid = computed(() =>
  form.value.firstName && form.value.lastName &&
  form.value.email && form.value.phone
)

function fmt(d) {
  if (!d) return ''
  return `${d.getMonth()+1}/${d.getDate()}/${String(d.getFullYear()).slice(2)}`
}

function handleConfirm() {
  if (!isValid.value) return
  emit('confirmed', { ...form.value })
  form.value = { firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '' }
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
