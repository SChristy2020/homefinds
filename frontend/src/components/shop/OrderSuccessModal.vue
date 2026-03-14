<template>
  <BaseModal :modelValue="modelValue" size="lg" noBackdropClose @update:modelValue="$emit('update:modelValue', $event)">
    <!-- Title -->
    <div class="success-title">{{ i18n.t('orderSuccess.title') }}</div>
    <div class="success-icon"><Gift :size="48" /></div>

    <template v-if="order">
      <!-- Greeting & Pickup Info -->
      <div class="greeting-block">
        <p class="greeting-line">
          <strong>Hi {{ order.firstName }}, {{ i18n.t('orderSuccess.greeting') }}</strong>
        </p>
        <p class="pickup-line">
          {{ i18n.t('orderSuccess.pickupInfo', { date: formattedPickup }) }}
          <em>{{ i18n.t('orderSuccess.pickupChangeablePrefix') }}<RouterLink class="orders-link" to="/orders">{{ i18n.t('orderSuccess.pickupChangeableLink') }}</RouterLink>{{ i18n.t('orderSuccess.pickupChangeableSuffix') }}</em>
        </p>
        <ul class="contact-list">
          <li>Name: <strong>{{ order.firstName }} {{ order.lastName }}</strong></li>
          <li>Email: <strong>{{ order.email }}</strong></li>
          <li>Phone: <strong>{{ order.phone }}</strong></li>
        </ul>
      </div>

      <!-- Payment Notice -->
      <div class="payment-notice">
        <p class="payment-title">
          <span class="warn-icon">⚠️</span> {{ i18n.t('orderSuccess.paymentTitle') }}
        </p>
        <ul>
          <li v-for="(note, i) in i18n.t('orderSuccess.paymentNotes')" :key="i" v-html="note"></li>
        </ul>
      </div>

      <!-- Zelle Info -->
      <div class="zelle-block">
        <p class="zelle-title">💰 {{ i18n.t('orderSuccess.zelleTitle') }}</p>
        <ul>
          <li>{{ i18n.t('guide.zelleAccount') }}</li>
          <li>{{ i18n.t('guide.zelleName') }}</li>
          <li>{{ i18n.t('orderSuccess.zelleNote') }}</li>
        </ul>
      </div>

      <!-- Order Number -->
      <p class="order-number-label">
        <strong>{{ i18n.t('orderSuccess.orderNumberLabel') }}</strong>
        <span class="order-number-value">{{ orderNumber }}</span>
      </p>

      <!-- Items Table -->
      <table class="items-table">
        <thead>
          <tr>
            <th class="col-num"></th>
            <th class="col-thumb">{{ i18n.t('cart.colThumb') }}</th>
            <th class="col-name">{{ i18n.t('cart.colName') }}</th>
            <th class="col-pickup">{{ i18n.t('cart.colPickup') }}</th>
            <th class="col-price">{{ i18n.t('cart.colPrice') }}</th>
            <th class="col-position">{{ i18n.t('orderSuccess.colPosition') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in order.items" :key="item.id">
            <td class="col-num">{{ index + 1 }}</td>
            <td class="col-thumb">
              <div class="item-thumb">
                <img v-if="item.images && item.images.length" :src="item.images[0].url" :alt="item.name" />
              </div>
            </td>
            <td class="col-name">{{ getItemName(item) }}</td>
            <td class="col-pickup">{{ formatPickupDate(item.pickupTime) }}</td>
            <td class="col-price">
              <span v-if="item.originalPrice" class="strikethrough">${{ item.originalPrice }}</span>
              ${{ item.price }}
            </td>
            <td class="col-position" :class="{ 'not-first': item.waitingPosition > 1 }">
              {{ positionLabel(item.waitingPosition) }}
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Total Summary -->
      <div class="total-summary">
        <span>{{ i18n.t('cart.itemCountPrefix') }}{{ order.items.length }}{{ i18n.t('cart.itemCountSuffix') }}</span>
        <span class="total-amount">
          <span v-if="totalOriginal > totalPrice" class="strikethrough">${{ totalOriginal }}</span>
          ${{ totalPrice }}
        </span>
      </div>

      <!-- Not-first warning -->
      <p v-if="hasNotFirst" class="not-first-warning">{{ i18n.t('orderSuccess.notFirstWarning') }}</p>

      <div class="section-divider"></div>

      <!-- Guide Section -->
      <ShoppingGuideContent />
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Gift } from 'lucide-vue-next'
import BaseModal from '@/components/shared/BaseModal.vue'
import ShoppingGuideContent from '@/components/shared/ShoppingGuideContent.vue'
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({ modelValue: Boolean, order: Object })
defineEmits(['update:modelValue'])
const i18n = useI18nStore()

function positionLabel(pos) {
  if (!pos) return ''
  const labels = i18n.t('orderSuccess.positionLabels')
  if (pos <= labels.length) return labels[pos - 1]
  return i18n.t('orderSuccess.positionFallback', { n: pos })
}

function getItemName(item) {
  const trans = item.translations
  if (trans) {
    const t = trans.find(t => t.locale === i18n.locale) || trans.find(t => t.locale === 'en')
    if (t?.name) return t.name
  }
  return item.name || item.code
}

function formatPickupDate(pickupTime) {
  if (!pickupTime) return i18n.t('cart.anytime')
  const d = new Date(pickupTime)
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}/${d.getFullYear()}`
}

const formattedPickup = computed(() => {
  if (!props.order?.estimatedPickup) return ''
  const ep = props.order.estimatedPickup
  const parts = ep.match(/(\d+)\/(\d+)\/(\d+)/)
  if (!parts) return ep
  const m = String(parts[1]).padStart(2, '0')
  const d = String(parts[2]).padStart(2, '0')
  const y = parts[3]
  return `${m}/${d}/${y}`
})

const totalPrice = computed(() =>
  props.order?.items.reduce((s, i) => s + i.price, 0) ?? 0
)

const totalOriginal = computed(() =>
  props.order?.items.reduce((s, i) => s + (i.originalPrice ?? i.price), 0) ?? 0
)

const hasNotFirst = computed(() =>
  props.order?.items.some(i => i.waitingPosition > 1) ?? false
)

const orderNumber = computed(() => {
  if (!props.order) return ''
  const shortId = String(props.order.id).slice(-6)
  const total = totalPrice.value
  const count = String(props.order.items.length).padStart(2, '0')
  return `S${shortId}${Math.floor(total)}${count}`
})
</script>

<style scoped>
.success-title {
  font-family: var(--font-display);
  font-size: 1.4rem; font-weight: 700;
  text-align: center; margin-bottom: 10px;
}
.success-icon { display: flex; justify-content: center; color: var(--accent); margin-bottom: 16px; }

/* Greeting */
.greeting-block { margin-bottom: 12px; font-size: 0.88rem; }
.greeting-line { margin-bottom: 4px; }
.pickup-line { color: var(--mid); margin-bottom: 6px; }
.pickup-line em { font-style: italic; }
.orders-link { color: var(--accent); text-decoration: underline; font-style: normal; }
.orders-link:hover { opacity: 0.8; }
.contact-list { list-style: disc; padding-left: 20px; margin: 0; }
.contact-list li { margin-bottom: 2px; }

/* Payment Notice */
.payment-notice {
  background: #fffbf0;
  border: 1.5px solid #f0d080;
  border-radius: var(--radius);
  padding: 10px 14px;
  margin-bottom: 12px;
  font-size: 0.83rem;
}
.payment-title {
  font-weight: 700;
  margin-bottom: 6px;
  font-size: 0.85rem;
}
.warn-icon { margin-right: 4px; }
.payment-notice ul { margin: 0; padding-left: 18px; }
.payment-notice li { margin-bottom: 4px; line-height: 1.5; }

/* Zelle Block */
.zelle-block {
  margin-bottom: 10px;
  font-size: 0.83rem;
}
.zelle-title { font-weight: 700; margin-bottom: 6px; }
.zelle-block ul { list-style: disc; padding-left: 20px; margin: 0; }
.zelle-block li { margin-bottom: 3px; }

/* Order Number */
.order-number-label {
  font-size: 0.88rem;
  font-weight: 700;
  margin-bottom: 12px;
}
.order-number-value {
  font-family: monospace;
  background: #f4f4f4;
  border-radius: 4px;
  padding: 2px 8px;
  margin-left: 6px;
  letter-spacing: 0.05em;
}

/* Items Table */
.items-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
  font-size: 0.85rem;
}
.items-table thead th {
  text-align: left;
  padding: 6px 6px;
  border-bottom: 1.5px solid var(--border);
  font-size: 0.8rem;
  color: #888;
  font-weight: 500;
}
.items-table tbody tr { border-bottom: 1px solid var(--border); }
.items-table tbody tr:last-child { border-bottom: none; }
.items-table tbody td { padding: 7px 6px; vertical-align: middle; }
.col-num { width: 22px; color: #999; font-size: 0.78rem; text-align: center; }
.col-thumb { width: 50px; }
.col-pickup { color: #666; }
.col-price { white-space: nowrap; font-weight: 600; text-align: right; }
.items-table thead th.col-price { text-align: right; }
.items-table thead th.col-position { text-align: center; }
.col-position { white-space: nowrap; font-weight: 600; text-align: center; font-size: 0.8rem; color: #2e7d32; vertical-align: middle; }
.col-position.not-first { color: #c0392b; }

.item-thumb {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, #2a2a2a 0%, #4a4040 100%);
  border-radius: 4px; overflow: hidden;
}
.item-thumb img { width: 100%; height: 100%; object-fit: cover; }

/* Total */
.total-summary {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 0 4px;
  font-size: 1rem; font-weight: 600;
}
.total-amount { font-size: 1.05rem; }

/* Not first warning */
.not-first-warning {
  color: #c0392b;
  font-size: 0.83rem;
  font-weight: 600;
  margin: 6px 0 0;
}

.strikethrough { text-decoration: line-through; color: #aaa; margin-right: 4px; font-weight: 400; }
</style>
