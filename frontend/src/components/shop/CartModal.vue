<template>
  <BaseModal :modelValue="modelValue" size="lg" @update:modelValue="$emit('update:modelValue', $event)">
    <h2 class="modal-title">{{ i18n.t('cart.title') }}</h2>

    <!-- Cart Items Table (only when not empty) -->
    <template v-if="cart.items.length > 0">
      <div class="cart-table-wrapper">
      <table class="cart-table">
        <thead>
          <tr>
            <th class="col-num"></th>
            <th class="col-thumb">{{ i18n.t('cart.colThumb') }}</th>
            <th class="col-name">{{ i18n.t('cart.colName') }}</th>
            <th class="col-pickup">{{ i18n.t('cart.colPickup') }}</th>
            <th class="col-price">{{ i18n.t('cart.colPrice') }}</th>
            <th class="col-delete"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in cart.items" :key="item.id" :class="{ 'row-sold-out': soldOutProductIds.includes(item.id) || duplicateProductIds.includes(item.id) }">
            <td class="col-num">{{ index + 1 }}</td>
            <td class="col-thumb">
              <div class="cart-thumb">
                <img v-if="item.images && item.images.length" :src="item.images[0].url" :alt="item.name" />
              </div>
            </td>
            <td class="col-name">
              {{ getItemName(item) }}
              <div v-if="duplicateProductIds.includes(item.id)" class="duplicate-item-error">{{ i18n.t('cart.alreadyReservedItem') }}</div>
              <div v-if="soldOutProductIds.includes(item.id)" class="duplicate-item-error">{{ i18n.t('cart.soldOutItem') }}</div>
            </td>
            <td class="col-pickup">{{ formatPickupDate(item.pickupTime) }}</td>
            <td class="col-price">
              <span v-if="item.originalPrice" class="strikethrough">${{ item.originalPrice }}</span>
              ${{ item.price }}
            </td>
            <td class="col-delete">
              <button class="btn-delete" :class="{ 'btn-delete--alert': soldOutProductIds.includes(item.id) || duplicateProductIds.includes(item.id) }" @click="cart.remove(item.id)"><Trash2 :size="15" /></button>
            </td>
          </tr>
        </tbody>
      </table>
      </div>

      <!-- Total Summary -->
      <div class="total-summary">
        <span>{{ i18n.t('cart.itemCountPrefix') }}{{ cart.count }}{{ i18n.t('cart.itemCountSuffix') }}</span>
        <span class="total-amount">
          <span v-if="totalOriginal > cart.total" class="strikethrough">${{ totalOriginal }}</span>
          ${{ cart.total }}
        </span>
      </div>
    </template>

    <!-- Empty state -->
    <div v-else class="empty-state">
      <div class="empty-state-icon"><ShoppingCart :size="40" /></div>
      <p>{{ i18n.t('cart.empty') }}</p>
    </div>

    <div class="section-divider"></div>

    <!-- Checkout Form -->
    <UserInfoForm v-model="form" :pickupWarningDate="pickupWarningDate" />

    <!-- Subscribe Marketing -->
    <div class="subscribe-row">
      <label class="subscribe-label">
        <input type="checkbox" v-model="subscribeMarketing" class="subscribe-checkbox" />
        {{ i18n.t('cart.subscribeMarketing') }}
      </label>
    </div>

    <!-- Reserve Button -->
    <div class="action-row">
      <button class="btn-primary" :disabled="!isValid" @click="handleConfirm">{{ i18n.t('cart.reserve') }}</button>
      <div v-if="soldOutProductIds.length" class="duplicate-btn-error">{{ i18n.t('cart.soldOutBtn') }}</div>
      <div v-if="duplicateProductIds.length" class="duplicate-btn-error">{{ i18n.t('cart.alreadyReservedBtn') }}</div>
    </div>

    <div class="section-divider"></div>

    <!-- Inline Guide Section -->
    <ShoppingGuideContent />
  </BaseModal>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { ShoppingCart, Trash2 } from 'lucide-vue-next'
import BaseModal from '@/components/shared/BaseModal.vue'
import UserInfoForm from '@/components/shared/UserInfoForm.vue'
import ShoppingGuideContent from '@/components/shared/ShoppingGuideContent.vue'
import { useCartStore } from '@/stores/cart'
import { useOrdersStore } from '@/stores/orders'
import { useProductsStore } from '@/stores/products'
import { useUserStore } from '@/stores/user'
import { useI18nStore } from '@/stores/i18n'

const FORM_USER_KEY = 'homefinds_form_user'

function loadSavedUser() {
  try { return JSON.parse(localStorage.getItem(FORM_USER_KEY)) || {} } catch { return {} }
}

const props = defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue'])

const cart = useCartStore()
const ordersStore = useOrdersStore()
const productsStore = useProductsStore()
const userStore = useUserStore()
const onOrderSuccess = inject('onOrderSuccess')
const i18n = useI18nStore()

const VALID_SALUTATIONS = ['Mr.', 'Ms.']
const resolveSalutation = (val) => VALID_SALUTATIONS.includes(val) ? val : 'Mr.'

const saved = loadSavedUser()
const cu = userStore.currentUser
const form = ref({
  firstName:        cu?.first_name   || saved.firstName   || '',
  lastName:         cu?.last_name    || saved.lastName    || '',
  salutation:       resolveSalutation(cu?.salutation || saved.salutation),
  email:            cu?.email        || saved.email       || '',
  phone:            cu?.phone        || saved.phone       || '',
  estimatedPickup:  '',
  zelleRefund:      cu?.zelle_refund || saved.zelleRefund || 'phone',
  zelleRefundOther: saved.zelleRefundOther || '',
})
const duplicateProductIds = ref([])
const soldOutProductIds = ref([])
const subscribeMarketing = ref(true)

// 當 modal 開啟時，從 localStorage / userStore 補填空白欄位
watch(() => props.modelValue, (open) => {
  if (!open) return
  const s = loadSavedUser()
  const cu = userStore.currentUser
  const f = form.value
  if (!f.firstName)        f.firstName        = cu?.first_name   || s.firstName   || ''
  if (!f.lastName)         f.lastName         = cu?.last_name    || s.lastName    || ''
  f.salutation = resolveSalutation(cu?.salutation || s.salutation || f.salutation)
  if (!f.email)            f.email            = cu?.email        || s.email       || ''
  if (!f.phone)            f.phone            = cu?.phone        || s.phone       || ''
  if (!f.zelleRefundOther) f.zelleRefundOther = s.zelleRefundOther || ''
})

// 當 user 身份欄位變動時清除重複錯誤
watch(() => [form.value.lastName, form.value.email, form.value.phone], () => {
  duplicateProductIds.value = []
  soldOutProductIds.value = []
})

const totalOriginal = computed(() =>
  parseFloat(cart.items.reduce((s, i) => s + (i.originalPrice ?? i.price), 0).toFixed(2))
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
  return `${String(minDay.getMonth() + 1).padStart(2, '0')}/${String(minDay.getDate()).padStart(2, '0')}/${minDay.getFullYear()}`
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
  const _d = new Date(pickupTime)
  const h = _d.getHours()
  const ampm = h >= 12 ? 'PM' : 'AM'
  const h12 = h % 12 || 12
  return `${String(_d.getMonth() + 1).padStart(2, '0')}/${String(_d.getDate()).padStart(2, '0')}/${_d.getFullYear()} ${h12}:${String(_d.getMinutes()).padStart(2, '0')} ${ampm}`
}

function getItemName(item) {
  const trans = item.translations
  if (trans) {
    const t = trans.find(t => t.locale === i18n.locale) || trans.find(t => t.locale === 'en')
    if (t?.name) return t.name
  }
  return item.name || item.code
}

async function handleConfirm() {
  if (!isValid.value) return
  duplicateProductIds.value = []
  soldOutProductIds.value = []

  // 檢查購物車商品是否已被設為 sold out
  const soldIds = cart.items
    .filter(item => {
      const p = productsStore.products.find(p => p.id === item.id)
      return p?.soldOut
    })
    .map(item => item.id)
  if (soldIds.length) {
    soldOutProductIds.value = soldIds
    return
  }
  const cartSnapshot = [...cart.items]
  const formSnapshot = { ...form.value }
  let order
  try {
    order = await ordersStore.createOrder(formSnapshot, cart.items, subscribeMarketing.value)
  } catch (err) {
    if (err.message === 'duplicate' && err.duplicateProductIds) {
      duplicateProductIds.value = err.duplicateProductIds
      return
    }
    throw err
  }

  // 補上用戶資訊和商品細節（後端回傳的 order 不含這些）
  const enriched = {
    ...order,
    firstName:       formSnapshot.firstName,
    lastName:        formSnapshot.lastName,
    salutation:      formSnapshot.salutation,
    email:           formSnapshot.email,
    phone:           formSnapshot.phone,
    estimatedPickup: formSnapshot.estimatedPickup,
    items: order.items.map(item => {
      const src = cartSnapshot.find(c => c.id === item.product_id) || {}
      return {
        ...item,
        price:           Number(item.price),
        originalPrice:   src.originalPrice ? Number(src.originalPrice) : undefined,
        name:            src.name,
        translations:    src.translations,
        images:          src.images,
        pickupTime:      src.pickupTime,
        waitingPosition: item.waiting_position,
      }
    }),
  }

  localStorage.setItem(FORM_USER_KEY, JSON.stringify({
    firstName:        formSnapshot.firstName,
    lastName:         formSnapshot.lastName,
    salutation:       formSnapshot.salutation,
    email:            formSnapshot.email,
    phone:            formSnapshot.phone,
    zelleRefund:      formSnapshot.zelleRefund,
    zelleRefundOther: formSnapshot.zelleRefundOther,
  }))

  cart.clear()
  emit('update:modelValue', false)
  onOrderSuccess(enriched)
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
.cart-table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin-bottom: 12px;
}
.cart-table {
  width: 100%;
  border-collapse: collapse;
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
.col-name { min-width: 120px; }
.col-pickup { min-width: 120px; color: #666; }
.col-price { white-space: nowrap; font-weight: 600; text-align: right; }
.cart-table thead th.col-price { text-align: right; }
.col-delete { width: 32px; text-align: center; }
.btn-delete {
  background: none; border: none; cursor: pointer;
  color: #bbb; padding: 4px; border-radius: 4px;
  display: inline-flex; align-items: center;
  transition: color 0.15s;
}
.btn-delete:hover { color: #c0392b; }
.btn-delete--alert { color: #c0392b; }

.row-sold-out { background-color: #f2f2f2; }

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
  flex-direction: column;
  align-items: flex-end;
  margin-top: 16px;
  margin-bottom: 20px;
}

.duplicate-item-error {
  font-size: 0.78rem;
  color: #c0392b;
  margin-top: 3px;
}

.duplicate-btn-error {
  font-size: 0.82rem;
  color: #c0392b;
  margin-top: 6px;
}

.subscribe-row {
  margin-top: 14px;
}
.subscribe-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: #555;
  cursor: pointer;
  user-select: none;
}
.subscribe-checkbox {
  width: 15px;
  height: 15px;
  cursor: pointer;
  accent-color: var(--light);
  flex-shrink: 0;
}

</style>
