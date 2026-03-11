<template>
  <BaseModal :modelValue="modelValue" size="lg" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">{{ i18n.t('cart.title') }}</h2>

    <div v-if="cart.items.length === 0" class="empty-state">
      <div class="empty-state-icon"><ShoppingCart :size="40" /></div>
      <p>{{ i18n.t('cart.empty') }}</p>
    </div>

    <template v-else>
      <!-- Cart Items Table -->
      <table class="cart-table">
        <thead>
          <tr>
            <th class="col-num"></th>
            <th class="col-thumb">{{ i18n.t('cart.colThumb') }}</th>
            <th class="col-name">{{ i18n.t('cart.colName') }}</th>
            <th class="col-pickup">{{ i18n.t('cart.colPickup') }}</th>
            <th class="col-price">{{ i18n.t('cart.colPrice') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in cart.items" :key="item.id">
            <td class="col-num">{{ index + 1 }}</td>
            <td class="col-thumb">
              <div class="cart-thumb">
                <img v-if="item.images && item.images.length" :src="item.images[0].url" :alt="item.name" />
              </div>
            </td>
            <td class="col-name">{{ getItemName(item) }}</td>
            <td class="col-pickup">{{ formatPickupDate(item.pickupTime) }}</td>
            <td class="col-price">
              <span v-if="item.originalPrice" class="strikethrough">${{ item.originalPrice }}</span>
              ${{ item.price }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Total Summary -->
      <div class="total-summary">
        <span>{{ i18n.t('cart.itemCountPrefix') }}{{ cart.count }}{{ i18n.t('cart.itemCountSuffix') }}</span>
        <span class="total-amount">
          <span v-if="totalOriginal > cart.total" class="strikethrough">${{ totalOriginal }}</span>
          ${{ cart.total }}
        </span>
      </div>

      <div class="section-divider"></div>

      <!-- Checkout Form -->
      <UserInfoForm v-model="form" :pickupWarningDate="pickupWarningDate" />

      <!-- Reserve Button -->
      <div class="action-row">
        <button class="btn-primary" :disabled="!isValid" @click="handleConfirm">{{ i18n.t('cart.reserve') }}</button>
      </div>

      <div class="section-divider"></div>

      <!-- Inline Guide Section -->
      <div class="guide-inline">
        <h3 class="guide-inline-title">{{ i18n.t('guide.sectionTitle') }}</h3>

        <div class="guide-step">
          <h4>{{ i18n.t('guide.step1Title') }}</h4>
          <ul>
            <li v-for="(item, i) in i18n.t('guide.step1Items')" :key="i">{{ item }}</li>
            <li class="warning">{{ i18n.t('guide.step1Warning') }}</li>
          </ul>
        </div>

        <div class="guide-step">
          <h4>{{ i18n.t('guide.step2Title') }}</h4>
          <p>{{ i18n.t('guide.step2Intro') }}</p>
          <ul>
            <li v-for="(item, i) in i18n.t('guide.step2Items').slice(0, 2)" :key="i">{{ item }}</li>
            <li>
              {{ i18n.t('guide.step2PayLabel') }}
              <div class="zelle-info">
                <span>{{ i18n.t('guide.zelleAccount') }}</span>
                <span>{{ i18n.t('guide.zelleName') }}</span>
              </div>
            </li>
            <li v-for="(item, i) in i18n.t('guide.step2Items').slice(2)" :key="'b'+i">{{ item }}</li>
          </ul>
        </div>

        <div class="guide-step">
          <h4>{{ i18n.t('guide.step3Title') }}</h4>
          <ul>
            <li v-for="(item, i) in i18n.t('guide.step3Items')" :key="i">{{ item }}</li>
          </ul>
        </div>

        <p class="guide-contact">
          {{ i18n.t('guide.contact') }}
          <a href="mailto:qsa8647332@gmail.com">qsa8647332@gmail.com</a>
        </p>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { ShoppingCart } from 'lucide-vue-next'
import BaseModal from '@/components/shared/BaseModal.vue'
import UserInfoForm from '@/components/shared/UserInfoForm.vue'
import { useCartStore } from '@/stores/cart'
import { useOrdersStore } from '@/stores/orders'
import { useI18nStore } from '@/stores/i18n'

defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue'])

const cart = useCartStore()
const ordersStore = useOrdersStore()
const onOrderSuccess = inject('onOrderSuccess')
const i18n = useI18nStore()

const form = ref({ firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '', estimatedPickup: '', zelleRefund: 'phone', zelleRefundOther: '' })

const totalOriginal = computed(() =>
  cart.items.reduce((s, i) => s + (i.originalPrice ?? i.price), 0)
)

const latestPickupTime = computed(() => {
  if (cart.items.length === 0) return null
  return cart.items.reduce((latest, item) => {
    const d = new Date(item.pickupTime)
    return d > latest ? d : latest
  }, new Date(cart.items[0].pickupTime))
})

// Compute warning label entirely here so reactivity is simple (string prop, no Date crossing)
const pickupWarningDate = computed(() => {
  const min = latestPickupTime.value
  const ep = form.value.estimatedPickup
  if (!min || !ep) return ''
  const parts = ep.match(/(\d+)\/(\d+)\/(\d+)\s+(\d+):(\d+)/)
  if (!parts) return ''
  const selected = new Date(+parts[3], +parts[1] - 1, +parts[2])
  selected.setHours(0, 0, 0, 0)
  const minDay = new Date(min); minDay.setHours(0, 0, 0, 0)
  if (selected >= minDay) return ''
  return `${minDay.getFullYear()}/${String(minDay.getMonth() + 1).padStart(2, '0')}/${String(minDay.getDate()).padStart(2, '0')}`
})

const NAME_RE  = /^[a-zA-Z\u4e00-\u9fff\u3400-\u4dbf\s-]+$/
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const isValid = computed(() => {
  const f = form.value
  return cart.items.length > 0 &&
    f.firstName && NAME_RE.test(f.firstName) &&
    f.lastName  && NAME_RE.test(f.lastName)  &&
    f.email     && EMAIL_RE.test(f.email)    &&
    f.phone     && f.phone.replace(/\D/g, '').length >= 7
})

function formatPickupDate(pickupTime) {
  if (!pickupTime) return i18n.t('cart.anytime')
  return new Date(pickupTime).toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

function getItemName(item) {
  const trans = item.translations
  if (trans) {
    const t = trans.find(t => t.locale === i18n.locale) || trans.find(t => t.locale === 'en')
    if (t?.name) return t.name
  }
  return item.name || item.code
}

function handleConfirm() {
  if (!isValid.value) return
  const order = ordersStore.addOrder({ ...form.value }, cart.items)
  cart.clear()
  emit('update:modelValue', false)
  onOrderSuccess(order)
  form.value = { firstName: '', lastName: '', salutation: 'Mr.', email: '', phone: '', estimatedPickup: '', zelleRefund: 'phone', zelleRefundOther: '' }
}
</script>

<style scoped>
.modal-title {
  font-family: var(--font-display);
  font-size: 1.25rem; font-weight: 600;
  margin-bottom: 20px;
}

/* Cart Table */
.cart-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 12px;
  font-size: 0.88rem;
}
.cart-table thead th {
  text-align: left;
  padding: 6px 8px;
  border-bottom: 1.5px solid var(--border);
  font-size: 0.82rem;
  color: #888;
  font-weight: 500;
}
.cart-table tbody tr {
  border-bottom: 1px solid var(--border);
}
.cart-table tbody tr:last-child { border-bottom: none; }
.cart-table tbody td {
  padding: 8px 8px;
  vertical-align: middle;
}
.col-num { width: 24px; color: #999; font-size: 0.8rem; text-align: center; }
.col-thumb { width: 52px; }
.col-pickup { color: #666; }
.col-price { white-space: nowrap; font-weight: 600; text-align: right; }
.cart-table thead th.col-price { text-align: right; }

.cart-thumb {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #2a2a2a 0%, #4a4040 100%);
  border-radius: 4px;
  overflow: hidden;
}
.cart-thumb img { width: 100%; height: 100%; object-fit: cover; }

/* Total */
.total-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0 14px;
  font-size: 1rem;
  font-weight: 600;
}
.total-amount { font-size: 1.1rem; }

/* Reserve Button */
.action-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
  margin-bottom: 20px;
}

/* Inline Guide */
.guide-inline {
  border-radius: var(--radius);
  font-size: 0.83rem;
}
.guide-inline-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--charcoal);
  margin: 0 0 12px;
}
.guide-step { margin-bottom: 12px; }
.guide-step h4 {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--accent, #c9a96e);
  margin: 0 0 6px;
}
.guide-step p {
  font-size: 0.82rem;
  color: #555;
  margin: 0 0 4px;
}
.guide-step ul {
  margin: 0;
  padding-left: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.guide-step li {
  font-size: 0.82rem;
  color: #444;
  line-height: 1.5;
}
.guide-step li.warning {
  color: #c0392b;
  font-weight: 600;
  list-style: none;
  margin-left: -16px;
}
.zelle-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 4px;
  padding: 6px 10px;
  border-radius: 6px;
  font-weight: 600;
  color: var(--charcoal);
}
.guide-contact {
  font-size: 0.82rem;
  color: #555;
  margin: 8px 0 0;
  padding-top: 10px;
  border-top: 1px solid #dde5ef;
}
.guide-contact a {
  color: var(--accent, #c9a96e);
  text-decoration: none;
}
.guide-contact a:hover { text-decoration: underline; }
</style>
