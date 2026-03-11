<template>
  <div>
    <div class="form-row">
      <div class="form-group" :class="{ 'has-error': touched.firstName && !validName(modelValue.firstName) }">
        <label>{{ i18n.t('userForm.firstName') }}</label>
        <input :value="modelValue.firstName" :placeholder="i18n.t('userForm.firstName')"
          @input="update('firstName', $event.target.value)"
          @blur="touched.firstName = true" />
        <span v-if="touched.firstName && !validName(modelValue.firstName)" class="field-error">{{ nameError }}</span>
      </div>
      <div class="form-group" :class="{ 'has-error': touched.lastName && !validName(modelValue.lastName) }">
        <label>{{ i18n.t('userForm.lastName') }}</label>
        <input :value="modelValue.lastName" :placeholder="i18n.t('userForm.lastName')"
          @input="update('lastName', $event.target.value)"
          @blur="touched.lastName = true" />
        <span v-if="touched.lastName && !validName(modelValue.lastName)" class="field-error">{{ nameError }}</span>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>{{ i18n.t('userForm.salutation') }}</label>
        <div class="radio-group">
          <label v-for="(key, i) in salutationKeys" :key="key">
            <input type="radio" :checked="modelValue.salutation === key" @change="update('salutation', key)" /> {{ salutationLabels[i] }}
          </label>
        </div>
      </div>
      <div class="form-group">
        <label>{{ i18n.t('userForm.estimatedPickup') }}</label>
        <span v-if="pickupWarningDate" class="field-error">{{ i18n.t('userForm.pickupWarningPrefix') }} {{ pickupWarningDate }}</span>
        <PickupDatePicker :modelValue="modelValue.estimatedPickup" :placeholder="i18n.t('userForm.estimatedPickupPlaceholder')" @update:modelValue="update('estimatedPickup', $event)" />
      </div>
    </div>
    <div class="form-group" :class="{ 'has-error': touched.email && !validEmail(modelValue.email) }">
      <label>Email</label>
      <input :value="modelValue.email" type="email" placeholder="your@email.com"
        @input="update('email', $event.target.value)"
        @blur="touched.email = true" />
      <span v-if="touched.email && !validEmail(modelValue.email)" class="field-error">{{ emailError }}</span>
    </div>
    <div class="form-group" :class="{ 'has-error': touched.phone && !validPhone(modelValue.phone) }">
      <label>{{ i18n.t('userForm.phone') }}</label>
      <input :value="modelValue.phone" :placeholder="i18n.t('userForm.phonePlaceholder')"
        @input="update('phone', $event.target.value)"
        @blur="touched.phone = true" />
      <span v-if="touched.phone && !validPhone(modelValue.phone)" class="field-error">{{ phoneError }}</span>
    </div>
    <div class="form-group">
      <label>{{ i18n.t('userForm.zelleRefundQ') }}</label>
      <div class="radio-group">
        <label><input type="radio" :checked="modelValue.zelleRefund === 'phone'" @change="update('zelleRefund', 'phone')" /> {{ i18n.t('userForm.zelleByPhone') }}</label>
        <label><input type="radio" :checked="modelValue.zelleRefund === 'email'" @change="update('zelleRefund', 'email')" /> {{ i18n.t('userForm.zelleByEmail') }}</label>
        <label><input type="radio" :checked="modelValue.zelleRefund === 'other'" @change="update('zelleRefund', 'other')" /> {{ i18n.t('userForm.zelleOther') }}</label>
      </div>
      <input
        v-if="modelValue.zelleRefund === 'other'"
        class="mt-8"
        :value="modelValue.zelleRefundOther"
        :placeholder="i18n.t('userForm.zelleOtherPlaceholder')"
        @input="update('zelleRefundOther', $event.target.value)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18nStore } from '@/stores/i18n'
import PickupDatePicker from '@/components/shared/PickupDatePicker.vue'

const props = defineProps({ modelValue: Object, pickupWarningDate: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue'])
const i18n = useI18nStore()

const salutationKeys = ['Mr.', 'Ms.']
const salutationLabels = computed(() => i18n.t('userForm.salutations'))

const touched = ref({ firstName: false, lastName: false, email: false, phone: false })

// Validation rules
const NAME_RE  = /^[a-zA-Z\u4e00-\u9fff\u3400-\u4dbf\s-]+$/
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validName(v)  { return !!v && NAME_RE.test(v) }
function validEmail(v) { return !!v && EMAIL_RE.test(v) }
function validPhone(v) { return !!v && v.replace(/\D/g, '').length >= 7 }

const isEn = computed(() => i18n.locale === 'en')
const nameError  = computed(() => isEn.value ? 'Only letters and hyphens allowed' : '只允許文字與連字號（-）')
const emailError = computed(() => isEn.value ? 'Please enter a valid email' : '請輸入有效的 Email')
const phoneError = computed(() => isEn.value ? 'Please enter a valid phone number' : '請輸入有效的電話號碼')

function update(field, value) {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}

// Expose validators so CartModal can use them
defineExpose({ validName, validEmail, validPhone })
</script>

<style scoped>
.has-error input { border-color: #e74c3c; }
.field-error {
  font-size: 0.72rem;
  color: #e74c3c;
  margin-top: 3px;
}
</style>
