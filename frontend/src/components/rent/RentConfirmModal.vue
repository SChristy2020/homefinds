<template>
  <BaseModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)">

    <!-- ───────────── STEP 1: Form ───────────── -->
    <template v-if="step === 1">

      <!-- Title -->
      <h2 class="modal-title">
        {{ i18n.t('rentConfirm.title') }}
      </h2>

      <hr class="divider" />

      <!-- Date row -->
      <div class="section-title">{{ i18n.t('rentConfirm.stayInfo') }}</div>
      <div class="date-row">
        <div class="date-col">
          <span class="date-label">{{ i18n.t('rent.checkIn') }}</span>
          <span class="date-value">{{ fmt(selection.start) }}</span>
        </div>
        <span class="date-arrow">→</span>
        <div class="date-col">
          <span class="date-label">{{ i18n.t('rent.checkOut') }}</span>
          <span class="date-value">{{ fmt(selection.end) }}</span>
        </div>
        <span class="nights-badge">{{ i18n.t('rentConfirm.total') }}{{ nights }}{{ i18n.t('rentConfirm.nights') }}</span>
      </div>

      <!-- Price section -->
      <div class="price-section">
        <div class="price-line">
          <span class="price-label">{{ i18n.t('rent.originalLabel') }}</span>
          <span class="price-value price-original">USD {{ originalPrice }}</span>
        </div>
        <div class="price-line">
          <span class="price-label">{{ i18n.t('rent.specialLabel') }}</span>
          <span class="price-value price-special">USD {{ specialPrice }}</span>
        </div>
        <div v-if="isEarlyBird" class="price-line early-bird-line">
          <span class="price-label early-bird-label">{{ i18n.t('rent.earlyBirdLabel') }}</span>
          <span class="price-value early-bird-price">USD {{ earlyBirdPrice }}</span>
          <span class="early-bird-note">{{ i18n.t('rent.earlyBirdNote') }}</span>
        </div>
      </div>

      <hr class="divider" />

      <!-- Basic info -->
      <div class="section-title">{{ i18n.t('rentConfirm.basicInfo') }}</div>

      <!-- Name row -->
      <div class="form-row">
        <div class="form-group" :class="{ 'has-error': touched.firstName && !validName(form.firstName) }">
          <label>{{ i18n.t('userForm.firstName') }}</label>
          <input v-model="form.firstName" :placeholder="i18n.t('userForm.firstName')" @blur="touched.firstName = true" />
          <span v-if="touched.firstName && !validName(form.firstName)" class="field-error">{{ nameError }}</span>
        </div>
        <div class="form-group" :class="{ 'has-error': touched.lastName && !validName(form.lastName) }">
          <label>{{ i18n.t('userForm.lastName') }}</label>
          <input v-model="form.lastName" :placeholder="i18n.t('userForm.lastName')" @blur="touched.lastName = true" />
          <span v-if="touched.lastName && !validName(form.lastName)" class="field-error">{{ nameError }}</span>
        </div>
      </div>

      <!-- Salutation -->
      <div class="form-group">
        <label>{{ i18n.t('userForm.salutation') }}</label>
        <div class="radio-group">
          <label v-for="(key, i) in salutationKeys" :key="key">
            <input type="radio" :checked="form.salutation === key" @change="form.salutation = key" /> {{ salutationLabels[i] }}
          </label>
        </div>
      </div>

      <!-- Email -->
      <div class="form-group" :class="{ 'has-error': touched.email && !validEmail(form.email) }">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="your@email.com" @blur="touched.email = true" />
        <span v-if="touched.email && !validEmail(form.email)" class="field-error">{{ emailError }}</span>
      </div>

      <!-- Phone -->
      <div class="form-group" :class="{ 'has-error': touched.phone && !validPhone(form.phone) }">
        <label>{{ i18n.t('userForm.phone') }}</label>
        <input v-model="form.phone" :placeholder="i18n.t('userForm.phonePlaceholder')" @blur="touched.phone = true" />
        <span v-if="touched.phone && !validPhone(form.phone)" class="field-error">{{ phoneError }}</span>
      </div>

      <!-- Birth year & Occupation -->
      <div class="form-row">
        <div class="form-group" :class="{ 'has-error': touched.birthYear && !validBirthYear(form.birthYear) }">
          <label>{{ i18n.t('rentConfirm.birthYear') }}</label>
          <input v-model="form.birthYear" type="number" :placeholder="i18n.t('rentConfirm.birthYearPlaceholder')" min="1930" max="2020" @blur="touched.birthYear = true" />
          <span v-if="touched.birthYear && !validBirthYear(form.birthYear)" class="field-error">{{ birthYearError }}</span>
        </div>
        <div class="form-group" :class="{ 'has-error': touched.occupation && !validOccupation(form.occupation) }">
          <label>{{ i18n.t('rentConfirm.occupation') }}</label>
          <input v-model="form.occupation" :placeholder="i18n.t('rentConfirm.occupationPlaceholder')" @blur="touched.occupation = true" />
          <span v-if="touched.occupation && !validOccupation(form.occupation)" class="field-error">{{ occupationError }}</span>
        </div>
      </div>

      <!-- Guests / Pets -->
      <div class="form-group">
        <label>{{ i18n.t('rentConfirm.guestsPets') }}</label>
        <div class="radio-group">
          <label><input type="radio" :checked="form.hasGuestsPets === true"  @change="form.hasGuestsPets = true"  /> {{ i18n.t('rentConfirm.yes') }}</label>
          <label><input type="radio" :checked="form.hasGuestsPets === false" @change="form.hasGuestsPets = false" /> {{ i18n.t('rentConfirm.no') }}</label>
        </div>
      </div>
      <div v-if="form.hasGuestsPets" class="form-group" :class="{ 'has-error': touched.guestsPetsDescription && !validGuestsDesc(form.guestsPetsDescription) }">
        <label>{{ i18n.t('rentConfirm.guestsPetsDesc') }}</label>
        <textarea v-model="form.guestsPetsDescription" :placeholder="i18n.t('rentConfirm.guestsPetsDescPlaceholder')" rows="3" @blur="touched.guestsPetsDescription = true"></textarea>
        <span v-if="touched.guestsPetsDescription && !validGuestsDesc(form.guestsPetsDescription)" class="field-error">{{ guestsDescError }}</span>
      </div>

      <!-- Special requests -->
      <div class="form-group">
        <label>{{ i18n.t('rentConfirm.specialRequests') }}</label>
        <span class="field-note field-note--alert">{{ i18n.t('rentConfirm.specialRequestsNote') }}</span>
        <textarea v-model="form.specialRequests" :placeholder="i18n.t('rentConfirm.specialRequestsPlaceholder')" rows="3"></textarea>
      </div>

      <!-- Confirm button -->
      <div style="margin-top: 16px;">
        <button class="btn-primary btn-block" :disabled="!isValid" @click="handleConfirm">{{ i18n.t('rentConfirm.confirmBtn') }}</button>
      </div>

      <!-- Policy -->
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

    </template>

    <!-- ───────────── STEP 2: Confirmation / Payment ───────────── -->
    <template v-else>

      <!-- scroll anchor -->
      <div ref="step2Top"></div>

      <!-- Title -->
      <h2 class="modal-title">
        {{ i18n.t('rentConfirm.confirmTitle') }}
      </h2>

      <!-- Home icon -->
      <div class="confirm-icon">
        <Home :size="40" color="#C4956A" />
      </div>

      <hr class="divider" />

      <!-- Basic info summary -->
      <div class="section-title">{{ i18n.t('rentConfirm.basicInfo') }}</div>
      <div class="info-grid">
        <span class="info-label">{{ i18n.t('userForm.firstName') }}</span>
        <span class="info-value">{{ form.firstName }}</span>

        <span class="info-label">{{ i18n.t('userForm.lastName') }}</span>
        <span class="info-value">{{ form.lastName }}</span>

        <span class="info-label">{{ i18n.t('rentConfirm.salutationLabel') }}</span>
        <span class="info-value">{{ form.salutation }}</span>

        <span class="info-label">Email</span>
        <span class="info-value">{{ form.email }}</span>

        <span class="info-label">{{ i18n.t('userForm.phone') }}</span>
        <span class="info-value">{{ form.phone }}</span>

        <span class="info-label">{{ i18n.t('rentConfirm.birthYear') }}</span>
        <span class="info-value">{{ form.birthYear }}</span>

        <span class="info-label">{{ i18n.t('rentConfirm.occupation') }}</span>
        <span class="info-value">{{ form.occupation }}</span>

        <span class="info-label">{{ i18n.t('rentConfirm.guestsPets') }}</span>
        <span class="info-value">{{ form.hasGuestsPets ? i18n.t('rentConfirm.yes') : i18n.t('rentConfirm.no') }}</span>

        <template v-if="form.hasGuestsPets && form.guestsPetsDescription">
          <span class="info-label">{{ i18n.t('rentConfirm.guestsPetsDesc') }}</span>
          <span class="info-value">{{ form.guestsPetsDescription }}</span>
        </template>

        <template v-if="form.specialRequests">
          <span class="info-label">{{ i18n.t('rentConfirm.specialRequests') }}</span>
          <span class="info-value">{{ form.specialRequests }}</span>
        </template>
      </div>

      <button class="btn-back" @click="step = 1">← {{ i18n.t('rentConfirm.backToEdit') }}</button>

      <hr class="divider" />

      <!-- Payment instructions -->
      <p class="pay-warning">
        <span class="warn-icon">⚠️</span>
        {{ i18n.t('rentConfirm.depositWarning') }}
      </p>
      <p class="pay-note">{{ i18n.t('rentConfirm.depositPayNote') }}</p>
      <div class="zelle-block">
        <p class="zelle-title">🔥 {{ i18n.t('rentConfirm.zelleInfo') }}</p>
        <ul>
          <li>帳號: (984)373-9392</li>
          <li>戶名: SHU CHING LI</li>
          <li>備註: 請務必註明您的「訂單編號」</li>
        </ul>
      </div>

      <hr class="divider" />

      <!-- Itinerary -->
      <div class="section-title">{{ i18n.t('rentConfirm.stayInfo') }}</div>

      <div class="order-no-row">
        <span class="order-no-label">{{ i18n.t('rentConfirm.orderNoLabel') }}：</span>
        <span class="order-no-value">{{ orderNumber }}</span>
      </div>

      <div class="date-row">
        <div class="date-col">
          <span class="date-label">{{ i18n.t('rent.checkIn') }}</span>
          <span class="date-value">{{ fmt(selection.start) }}</span>
        </div>
        <span class="date-arrow">→</span>
        <div class="date-col">
          <span class="date-label">{{ i18n.t('rent.checkOut') }}</span>
          <span class="date-value">{{ fmt(selection.end) }}</span>
        </div>
        <span class="nights-badge">{{ i18n.t('rentConfirm.total') }}{{ nights }}{{ i18n.t('rentConfirm.nights') }}</span>
      </div>

      <!-- Prices -->
      <div class="price-section">
        <div class="price-line">
          <span class="price-label">{{ i18n.t('rent.originalLabel') }}</span>
          <span class="price-value price-original">USD {{ originalPrice }}</span>
        </div>
        <div class="price-line">
          <span class="price-label">{{ i18n.t('rent.specialLabel') }}</span>
          <span class="price-value price-special">USD {{ specialPrice }}</span>
        </div>
        <div v-if="isEarlyBird" class="price-line early-bird-line">
          <span class="price-label early-bird-label">{{ i18n.t('rent.earlyBirdLabel') }}</span>
          <span class="price-value early-bird-price">USD {{ earlyBirdPrice }}</span>
          <span class="early-bird-note">{{ i18n.t('rent.earlyBirdNote') }}</span>
        </div>
      </div>

      <!-- Deposit amount -->
      <div class="deposit-row">
        <span class="deposit-label">{{ i18n.t('rentConfirm.depositAmountLabel') }}</span>
        <span class="deposit-amount">USD {{ depositAmount }}</span>
        <span class="deposit-note">{{ i18n.t('rentConfirm.depositAmountNote') }}</span>
      </div>

      <p class="auto-cancel-note">{{ i18n.t('rentConfirm.autoCancelNote') }}</p>

      <!-- Notify button -->
      <div style="margin-top: 16px;">
        <p v-if="apiError" class="api-error">{{ apiError }}</p>
        <button class="btn-primary btn-block" :disabled="loading" @click="handleNotify">
          {{ loading ? '提交中...' : i18n.t('rentConfirm.notifyBtn') }}
        </button>
      </div>

      <!-- Policy -->
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

    </template>

  </BaseModal>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { Home } from 'lucide-vue-next'
import BaseModal from '@/components/shared/BaseModal.vue'
import { useI18nStore } from '@/stores/i18n'
import { api } from '@/utils/api'

const props = defineProps({
  modelValue:    Boolean,
  selection:     Object,
  nights:        Number,
  totalPrice:    Number,  // final price (after early bird if applicable)
  originalPrice: { type: Number, default: 0 },
  specialPrice:  { type: Number, default: 0 },
  earlyBirdPrice:{ type: Number, default: 0 },
  isEarlyBird:   { type: Boolean, default: false },
  bookingDescription: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue', 'confirmed'])

const i18n = useI18nStore()

const step = ref(1)
const loading = ref(false)
const apiError = ref('')
const orderNumber = ref('')
const step2Top = ref(null)

// Reset step when modal closes
watch(() => props.modelValue, (val) => {
  if (!val) { step.value = 1; apiError.value = ''; orderNumber.value = '' }
})

const salutationKeys   = ['Mr.', 'Ms.']
const salutationLabels = computed(() => i18n.t('userForm.salutations'))

const depositAmount = computed(() => Math.round(props.totalPrice * 0.3))

const emptyForm = () => ({
  firstName: '', lastName: '', salutation: 'Mr.',
  email: '', phone: '',
  birthYear: '', occupation: '',
  hasGuestsPets: false, guestsPetsDescription: '',
  specialRequests: '',
})
const form    = ref(emptyForm())
const touched = ref({
  firstName: false, lastName: false, email: false, phone: false,
  birthYear: false, occupation: false, guestsPetsDescription: false,
})

const NAME_RE  = /^[a-zA-Z\u4e00-\u9fff\u3400-\u4dbf\s-]+$/
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validName(v)      { return !!v && NAME_RE.test(v) }
function validEmail(v)     { return !!v && EMAIL_RE.test(v) }
function validPhone(v)     { return !!v && v.replace(/\D/g, '').length >= 7 }
function validBirthYear(v) { const n = Number(v); return !!v && Number.isInteger(n) && n >= 1930 && n <= 2020 }
function validOccupation(v){ return !!v && v.trim().length > 0 }
function validGuestsDesc(v){ return !!v && v.trim().length > 0 }

const nameError       = computed(() => i18n.t('rentConfirm.errorName'))
const emailError      = computed(() => i18n.t('rentConfirm.errorEmail'))
const phoneError      = computed(() => i18n.t('rentConfirm.errorPhone'))
const birthYearError  = computed(() => i18n.t('rentConfirm.errorBirthYear'))
const occupationError = computed(() => i18n.t('rentConfirm.errorRequired'))
const guestsDescError = computed(() => i18n.t('rentConfirm.errorGuestsDesc'))

const isValid = computed(() =>
  validName(form.value.firstName) && validName(form.value.lastName) &&
  validEmail(form.value.email) && validPhone(form.value.phone) &&
  validBirthYear(form.value.birthYear) && validOccupation(form.value.occupation) &&
  (!form.value.hasGuestsPets || validGuestsDesc(form.value.guestsPetsDescription))
)

function fmt(d) {
  if (!d) return ''
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
}

function fmtDate(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

async function handleConfirm() {
  Object.keys(touched.value).forEach(k => touched.value[k] = true)
  if (!isValid.value) return

  loading.value = true
  apiError.value = ''
  try {
    const user = await api.post('/api/users', {
      first_name:  form.value.firstName,
      last_name:   form.value.lastName,
      salutation:  form.value.salutation,
      email:       form.value.email,
      phone:       form.value.phone,
      zelle_refund: 'phone',
      locale:      i18n.locale,
    })

    const reservation = await api.post('/api/reservations', {
      user_id:                 user.id,
      check_in:                fmtDate(props.selection.start),
      check_out:               fmtDate(props.selection.end),
      nights:                  props.nights,
      deposit_amount:          depositAmount.value,
      total_price:             props.totalPrice,
      birth_year:              parseInt(form.value.birthYear),
      occupation:              form.value.occupation,
      has_guests_or_pets:      form.value.hasGuestsPets,
      guests_pets_description: form.value.guestsPetsDescription || null,
      special_requests:        form.value.specialRequests || null,
    })

    orderNumber.value = reservation.order_number
    step.value = 2
    await nextTick()
    step2Top.value?.closest('.modal')?.scrollTo({ top: 0, behavior: 'instant' })
  } catch (e) {
    apiError.value = e.detail || '提交失敗，請再試一次'
  } finally {
    loading.value = false
  }
}

function handleNotify() {
  emit('confirmed', { ...form.value, orderNumber: orderNumber.value })
  form.value = emptyForm()
  touched.value = { firstName: false, lastName: false, email: false, phone: false,
                    birthYear: false, occupation: false, guestsPetsDescription: false }
  step.value = 1
}
</script>

<style scoped>
.modal-title {
  font-family: var(--font-display);
  font-size: 1.25rem; font-weight: 600; margin-bottom: 12px;
}
.title-en { font-size: 1rem; font-weight: 400; color: var(--mid); margin-left: 6px; }

.confirm-icon { text-align: center; margin: 8px 0 4px; }

/* Date row */
.date-row { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.date-col { display: flex; flex-direction: column; gap: 1px; }
.date-label { font-size: 0.75rem;  }
.date-value { font-size: 0.95rem; font-weight: 600; color: var(--charcoal); }
.date-arrow { font-size: 1.1rem; color: var(--mid); padding: 0 2px; margin-top: 10px; }
.nights-badge { margin-left: auto; font-size: 0.9rem; font-weight: 600; color: var(--charcoal); white-space: nowrap; }

/* Price section */
.price-section { display: flex; flex-direction: column; gap: 2px; margin-bottom: 12px; }
.price-line { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
.price-label { font-size: 0.9rem; color: var(--charcoal); min-width: 5em; }
.price-value { font-size: 1rem; }
.price-original { color: var(--mid); text-decoration: line-through; }
.price-special { font-size: 1.4rem; font-weight: 700; color: var(--charcoal); }
.early-bird-line { color: #c0392b; }
.early-bird-label { font-weight: 600; color: #c0392b; }
.early-bird-price { font-size: 1.4rem; font-weight: 800; color: #c0392b; }
.early-bird-note { font-size: 0.85rem; font-weight: 500; color: #c0392b; }

.divider { border: none; border-top: 1.5px solid var(--border); margin: 12px 0; }

.section-title { font-weight: 600; font-size: 1rem; margin-bottom: 10px; color: var(--charcoal); }

/* Form */
.form-row { display: flex; gap: 12px; }
.form-row .form-group { flex: 1; }
.form-group { margin-bottom: 12px; display: flex; flex-direction: column; gap: 4px; }
.form-group label { font-size: 0.95rem; color: var(--charcoal); font-weight: 500; }
.form-group input, .form-group textarea {
  border: 1px solid var(--border); border-radius: 6px;
  padding: 8px 10px; font-size: 0.9rem; width: 100%; box-sizing: border-box;
  background: var(--surface, #fafafa);
}
.form-group input[type="number"] { -moz-appearance: textfield; }
.form-group input[type="number"]::-webkit-outer-spin-button,
.form-group input[type="number"]::-webkit-inner-spin-button { -webkit-appearance: none; }
.form-group textarea { resize: vertical; }
.has-error input, .has-error textarea { border-color: #e74c3c; }
.field-error { font-size: 0.72rem; color: #e74c3c; }
.field-note { font-size: 0.82rem; color: var(--mid); }
.field-note--alert { color: #c0392b; font-weight: 600; }

.radio-group { display: flex; gap: 16px; flex-wrap: wrap; font-size: 0.9rem; }
.radio-group label { display: flex; align-items: center; gap: 4px; cursor: pointer; white-space: nowrap; }

.btn-block { width: 100%; }

/* Info grid (step 2 summary) */
.info-grid {
  display: grid;
  grid-template-columns: minmax(0, 4fr) minmax(0, 8fr);
  gap: 6px 12px;
  margin-bottom: 12px;
  font-size: 0.9rem;
}
.info-label { color: var(--mid); }
.info-value { color: var(--charcoal); font-weight: 500; word-break: break-all; }

/* Back button */
.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 4px;
  padding: 7px 18px;
  font-size: 0.86rem;
  font-family: var(--font-body);
  font-weight: 500;
  letter-spacing: 0.03em;
  color: var(--accent);
  background: transparent;
  border: 1.5px solid var(--accent);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
}
.btn-back:hover {
  background: var(--accent-light);
}

/* Payment block */
.pay-warning {
  font-size: 0.9rem;
  color: var(--charcoal);
  margin-bottom: 4px;
  display: flex;
  align-items: flex-start;
  gap: 5px;
  font-weight: 700;
}
.warn-icon { flex-shrink: 0; }
.pay-note { font-size: 0.88rem; margin-bottom: 8px; }

.zelle-block {
  background: var(--surface, #fafafa);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 4px;
  font-size: 0.88rem;
}
.zelle-title { font-weight: 600; color: var(--charcoal); margin-bottom: 4px; }
.zelle-block ul { list-style: disc; padding-left: 1.4em; margin: 0; }
.zelle-block li { margin-bottom: 2px; color: var(--charcoal); }

/* Order number */
.order-no-row { display: flex; align-items: center; gap: 6px; margin-bottom: 8px; font-size: 0.95rem; font-weight: 700; }
.order-no-label {}
.order-no-value { font-weight: 700; color: var(--charcoal); letter-spacing: 0.04em; }

/* Deposit row */
.deposit-row {
  display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;}
.deposit-label { font-size: 0.9rem; color: var(--charcoal); min-width: 5em;}
.deposit-amount { font-size: 1.4rem; font-weight: 800; color: var(--charcoal); }
.deposit-note { font-size: 0.82rem; color: #c0392b; font-weight: 500; }

.auto-cancel-note {
  font-size: 0.82rem; color: #c0392b; font-weight: 700; padding: 1rem 0 0 0;
}
.api-error {
  font-size: 0.85rem; color: #c0392b; margin-bottom: 8px; font-weight: 600;
}

/* Policy */
.policy {
  font-size: 0.9rem;
  margin-top: 12px; padding-top: 12px;
  border-top: 1.5px solid var(--border);
}
.policy p { margin-bottom: 3px; }
.policy strong { color: var(--charcoal); }
.policy-row { display: flex; gap: 10px; margin-bottom: 2px; }
.days { font-weight: 600; color: var(--charcoal); min-width: 100px; }
.policy :deep(ul), .policy :deep(ol) { padding-left: 1.5em; margin: 4px 0; }
.policy :deep(ul) { list-style-type: disc; }
.policy :deep(ol) { list-style-type: decimal; }
.policy :deep(ul ul) { list-style-type: circle; }
.policy :deep(ul ul ul) { list-style-type: square; }
.policy :deep(blockquote) { margin-left: 1.5em; padding-left: 0.75em; border-left: 3px solid var(--border); }
.policy :deep(iframe) { width: 100% !important; max-width: 100%; height: 200px; border: none; border-radius: 6px; display: block; margin: 8px 0; }
.policy :deep(.map-embed) { width: 100%; }
</style>
